import traceback
from sensors import distance_sensor
from computer_vision import vision
from computer_vision.core import webcam
from controller import gap_logic, green_logic, line_follower, obstacle_logic, red_logic
from controller.core import basic_movements
from openrdk import CommsRuntime
from time import sleep

# Run with "PYTHONPATH=open_rdk/host/main/src python3 main.py"
# View webcam at "http://localhost:5000"

def main():
    capture = webcam.get_webcam()
    openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)

    sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    left_motor = openrdk.traction(openrdk.get_serial_by_name("left_motor"))
    right_motor = openrdk.traction(openrdk.get_serial_by_name("right_motor"))
    #distance_sensor = openrdk.distance_sensor(openrdk.get_serial_by_name("distance_sensor_module"))
    
    previous_green_detected = False
    previous_red_detected = False
    previous_gap_detected = False
    previous_obstacle_detected = False

    while True:
        try:
            line_info, green_dispersion, red_on_track = vision.update(capture)
            #obstacle_on_track = distance_sensor.update(distance_sensor)
            line_follower.update(line_info, left_motor, right_motor)
            gap_logic.update(line_info, left_motor, right_motor)

            green_detected = any(green_dispersion.values())

            if green_detected and not previous_green_detected:
                basic_movements.go_straight_shorter(left_motor, right_motor)

                sleep(2.0)

                green_frame_count = 10
                green_detection_counts = {
                    "top_left": 0,
                    "top_right": 0,
                    "bottom_left": 0,
                    "bottom_right": 0
                }

                for _ in range(green_frame_count):
                    line_info, current_green_dispersion, red_on_track = vision.update(capture)
                    print(f">>> GREEN CHECK: {current_green_dispersion}")

                    for position, detected in current_green_dispersion.items():
                        green_detection_counts[position] += int(detected)

                    sleep(0.05)

                minimum_confirmations = green_frame_count // 2 + 1
                confirmed_green_dispersion = {
                    position: count >= minimum_confirmations
                    for position, count in green_detection_counts.items()
                }

                green_dispersion = confirmed_green_dispersion
                print(
                    f">>> CONFIRMED GREEN: {green_dispersion} "
                    f"({green_detection_counts}/{green_frame_count})"
                )

                green_detected = any(green_dispersion.values())
                if green_detected:
                    green_logic.update(green_dispersion, left_motor, right_motor)

            previous_green_detected = green_detected
            
            if red_on_track:
                red_logic.update(left_motor, right_motor)

            previous_red_detected = red_on_track

            #if obstacle_on_track:
            #    obstacle_logic.update(left_motor, right_motor)

            #previous_obstacle_detected = obstacle_on_track


            sleep(0.1)

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