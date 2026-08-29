import time
import traceback
from sensors import distance_sensor
from computer_vision import vision
from computer_vision.core import webcam
from controller import gap_logic, green_logic, line_follower, obstacle_logic, red_logic
from openrdk import CommsRuntime

# Run with "PYTHONPATH=open_rdk/host/main/src python3 main.py"

def main():
    """Start the robot runtime and continuously execute its control loop."""

    capture = webcam.get_webcam()
    openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)

    time.sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    left_motor = openrdk.traction(openrdk.get_serial_by_name("left_motor"))
    right_motor = openrdk.traction(openrdk.get_serial_by_name("right_motor"))
    distance_sensor_module = openrdk.distance_sensor(openrdk.get_serial_by_name("distance_sensor_module"))

    stable_samples = 0
    target_latency_ms = 35.0
    startup_deadline = time.perf_counter() + 15.0

    print("Waiting for camera latency to stabilize before starting robot loop...")
    while time.perf_counter() < startup_deadline:
        start_time = time.perf_counter()
        frame_result = vision.update(capture)
        latency_ms = (time.perf_counter() - start_time) * 1000

        if frame_result is not None and latency_ms <= target_latency_ms:
            stable_samples += 1
            if stable_samples >= 10:
                print(f"Latency stable: {latency_ms:.2f} ms; starting robot loop.")
                break
        else:
            stable_samples = 0

        time.sleep(0.05)
    else:
        print("Startup latency did not stabilize within deadline; starting robot loop anyway.")

    previous_green_detected = False
    previous_gap_detected = False
    previous_obstacle_detected = False

    while True:
        try:
            start_time = time.perf_counter()

            line_info, green_dispersion, red_on_track = vision.update(capture)
            obstacle_on_track = distance_sensor.update(distance_sensor_module)
            line_follower.update(line_info, left_motor, right_motor)
            gap_logic.update(line_info, left_motor, right_motor)

            green_detected = any(green_dispersion.values())

            if green_detected and not previous_green_detected:
                green_detected, confirmed_green_dispersion = green_logic.do_second_green_check(capture, vision, left_motor, right_motor)

                if green_detected:
                    green_logic.update(confirmed_green_dispersion, left_motor, right_motor)

            previous_green_detected = green_detected
            
            if red_on_track:
                red_logic.update(left_motor, right_motor)

            if obstacle_on_track:
                obstacle_logic.update(left_motor, right_motor)

            previous_obstacle_detected = obstacle_on_track

            loop_time = time.perf_counter() - start_time
            print(f"Loop: {loop_time * 1000:.2f} ms")

            time.sleep(0.1)

        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Stopping execution...")
            
            left_motor.stop()
            right_motor.stop()
            openrdk.stop()
            
            exit()
        
        except Exception as e:
            tb = e.__traceback__
            error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

            print(f"Error {e} occurred in {error_file} at function {function} at line {error_line}: {text}")
            print("Stopping execution...")
            
            left_motor.stop()
            right_motor.stop()
            openrdk.stop()
            
            exit()

if __name__ == "__main__":
    main()