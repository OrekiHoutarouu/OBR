import traceback
import threading
import time

from computer_vision import vision
from computer_vision.core import webcam
from controller import green_logic, line_follower
from controller.core import basic_movements
from openrdk import CommsRuntime
from time import sleep


# Run with "PYTHONPATH=open_rdk/host/main/src python3 main.py"
# View webcam at "http://localhost:5000"

MOTOR_UPDATE_HZ = 15

GREEN_FRAME_COUNT = 10


def main():
    capture = webcam.get_webcam()

    openrdk = CommsRuntime(
        auto_start=True,
        enable_webview=True,
        enable_webview_updates=True
    )

    # Wait for the devices to come online
    sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    left_motor = openrdk.traction(
        openrdk.get_serial_by_name("left_motor")
    )

    right_motor = openrdk.traction(
        openrdk.get_serial_by_name("right_motor")
    )

    # ------------------------------------------------------------------
    # Shared vision data
    # ------------------------------------------------------------------

    shared_data = {
        "line_info": None,
        "green_dispersion": None,
        "frame_id": 0
    }

    data_lock = threading.Lock()

    # Condition lets threads WAIT for a new vision frame instead of
    # continuously polling shared_data.
    vision_condition = threading.Condition(data_lock)

    stop_event = threading.Event()

    # When set, green behavior owns the motors.
    green_active = threading.Event()


    # ------------------------------------------------------------------
    # VISION THREAD
    # ------------------------------------------------------------------

    def vision_thread():
        try:
            while not stop_event.is_set():

                result = vision.update(capture)

                # vision.update() can return None if no frame was captured
                if result is None:
                    continue

                line_info, green_dispersion, _ = result

                # Publish line + green information from THE SAME FRAME
                with vision_condition:

                    shared_data["line_info"] = line_info
                    shared_data["green_dispersion"] = green_dispersion

                    shared_data["frame_id"] += 1

                    # Wake anything waiting for a fresh frame
                    vision_condition.notify_all()

        except Exception as e:
            tb = e.__traceback__
            error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

            print(
                f"Vision thread error {e} occurred in {error_file} "
                f"at function {function} at line {error_line}: {text}"
            )

            stop_event.set()

            with vision_condition:
                vision_condition.notify_all()


    # ------------------------------------------------------------------
    # LINE FOLLOWER THREAD
    # ------------------------------------------------------------------

    def line_follower_thread():
        try:
            update_interval = 1.0 / MOTOR_UPDATE_HZ
            next_update = time.monotonic()

            while not stop_event.is_set():

                # Green has priority over normal line following.
                if not green_active.is_set():

                    with data_lock:
                        line_info = shared_data["line_info"]

                    if line_info is not None:
                        line_follower.update(
                            line_info,
                            left_motor,
                            right_motor
                        )

                # ------------------------------------------------------
                # Fixed 15 Hz motor update
                # ------------------------------------------------------

                next_update += update_interval

                remaining_time = next_update - time.monotonic()

                if remaining_time > 0:
                    stop_event.wait(remaining_time)

                else:
                    # If an update took too long, DO NOT try to catch up
                    # by sending several commands quickly.
                    next_update = time.monotonic()

        except Exception as e:
            tb = e.__traceback__
            error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

            print(
                f"Line follower thread error {e} occurred in {error_file} "
                f"at function {function} at line {error_line}: {text}"
            )

            stop_event.set()

            with vision_condition:
                vision_condition.notify_all()


    # ------------------------------------------------------------------
    # GREEN THREAD
    # ------------------------------------------------------------------

    def green_thread():
        try:
            previous_green_detected = False
            last_frame_id = -1

            while not stop_event.is_set():

                # ------------------------------------------------------
                # WAIT FOR A NEW VISION FRAME
                #
                # This is important.
                #
                # The old version continuously hammered shared_data,
                # which could consume CPU and interfere with the vision
                # and line follower threads.
                # ------------------------------------------------------

                with vision_condition:

                    vision_condition.wait_for(
                        lambda:
                            shared_data["frame_id"] != last_frame_id
                            or stop_event.is_set()
                    )

                    if stop_event.is_set():
                        break

                    line_info = shared_data["line_info"]
                    green_dispersion = shared_data["green_dispersion"]
                    current_frame_id = shared_data["frame_id"]

                last_frame_id = current_frame_id

                if line_info is None or green_dispersion is None:
                    continue

                # ------------------------------------------------------
                # ONLY CONSIDER GREEN AT A TURN / CROSSROAD
                #
                # From the vision.py you gave me:
                #
                # touches_left  = black reaches left edge
                # touches_right = black reaches right edge
                #
                # One side  -> possible turn / branch
                # Both      -> possible crossroads
                #
                # On an ordinary straight section, green is ignored.
                # ------------------------------------------------------

                turn_or_crossroads = (
                    line_info["touches_left"]
                    or line_info["touches_right"]
                )

                if not turn_or_crossroads:
                    previous_green_detected = False
                    continue

                # Green only matters after the black-line geometry says
                # we're at a possible turn/crossroads.
                green_detected = any(green_dispersion.values())

                # Same rising-edge behavior as your original code
                if not (
                    green_detected
                    and not previous_green_detected
                ):
                    previous_green_detected = green_detected
                    continue

                # ------------------------------------------------------
                # GREEN CANDIDATE FOUND
                # ------------------------------------------------------

                green_active.set()

                try:
                    basic_movements.go_straight_shorter(
                        left_motor,
                        right_motor
                    )

                    sleep(2.0)

                    green_detection_counts = {
                        "top_left": 0,
                        "top_right": 0,
                        "bottom_left": 0,
                        "bottom_right": 0
                    }

                    # We now require 10 ACTUAL NEW vision frames.
                    confirmation_frame_id = last_frame_id

                    frames_collected = 0

                    while (
                        frames_collected < GREEN_FRAME_COUNT
                        and not stop_event.is_set()
                    ):

                        with vision_condition:

                            vision_condition.wait_for(
                                lambda:
                                    shared_data["frame_id"]
                                    != confirmation_frame_id
                                    or stop_event.is_set()
                            )

                            if stop_event.is_set():
                                break

                            current_line_info = (
                                shared_data["line_info"]
                            )

                            current_green_dispersion = (
                                shared_data["green_dispersion"]
                            )

                            confirmation_frame_id = (
                                shared_data["frame_id"]
                            )

                        if (
                            current_line_info is None
                            or current_green_dispersion is None
                        ):
                            continue

                        print(
                            f">>> GREEN CHECK: "
                            f"{current_green_dispersion}"
                        )

                        for position, detected in (
                            current_green_dispersion.items()
                        ):
                            green_detection_counts[position] += int(
                                detected
                            )

                        frames_collected += 1

                    if stop_event.is_set():
                        break

                    minimum_confirmations = (
                        GREEN_FRAME_COUNT // 2 + 1
                    )

                    confirmed_green_dispersion = {
                        position: count >= minimum_confirmations
                        for position, count
                        in green_detection_counts.items()
                    }

                    print(
                        f">>> CONFIRMED GREEN: "
                        f"{confirmed_green_dispersion} "
                        f"({green_detection_counts}/"
                        f"{GREEN_FRAME_COUNT})"
                    )

                    green_detected = any(
                        confirmed_green_dispersion.values()
                    )

                    if green_detected:
                        green_logic.update(
                            confirmed_green_dispersion,
                            left_motor,
                            right_motor
                        )

                finally:
                    green_active.clear()

                # ------------------------------------------------------
                # Get the CURRENT green state after the maneuver.
                #
                # This prevents immediately retriggering using stale
                # green information from before/during the maneuver.
                # ------------------------------------------------------

                with data_lock:
                    current_green = shared_data["green_dispersion"]

                if current_green is not None:
                    previous_green_detected = any(
                        current_green.values()
                    )
                else:
                    previous_green_detected = False

        except Exception as e:
            tb = e.__traceback__
            error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

            print(
                f"Green thread error {e} occurred in {error_file} "
                f"at function {function} at line {error_line}: {text}"
            )

            green_active.clear()
            stop_event.set()

            with vision_condition:
                vision_condition.notify_all()


    # ------------------------------------------------------------------
    # START THREADS
    # ------------------------------------------------------------------

    vision_worker = threading.Thread(
        target=vision_thread,
        daemon=True
    )

    line_follower_worker = threading.Thread(
        target=line_follower_thread,
        daemon=True
    )

    green_worker = threading.Thread(
        target=green_thread,
        daemon=True
    )

    vision_worker.start()
    line_follower_worker.start()
    green_worker.start()


    # ------------------------------------------------------------------
    # MAIN THREAD
    # ------------------------------------------------------------------

    try:
        stop_event.wait()

    except KeyboardInterrupt:
        print(
            "KeyboardInterrupt received. "
            "Stopping execution..."
        )

        stop_event.set()

        with vision_condition:
            vision_condition.notify_all()

    finally:
        left_motor.stop()
        right_motor.stop()
        openrdk.stop()


if __name__ == "__main__":
    main()
