import traceback
from sensors import distance_sensor
from computer_vision import vision
from computer_vision.core import webcam
from controller import gap_logic, green_logic, line_follower, obstacle_logic, red_logic
from openrdk import CommsRuntime
from time import sleep

# Run with "PYTHONPATH=open_rdk/host/main/src python3 main.py"

def main():
    """Start the robot runtime and continuously execute its control loop."""

    capture = webcam.get_webcam()
    openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)

    sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    left_motor = openrdk.traction(openrdk.get_serial_by_name("left_motor"))
    right_motor = openrdk.traction(openrdk.get_serial_by_name("right_motor"))
    #distance_sensor = openrdk.distance_sensor(openrdk.get_serial_by_name("distance_sensor_module"))
    
    previous_green_detected = False
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
                green_detected = green_logic.do_second_green_check(capture, vision, left_motor, right_motor)

                if green_detected:
                    green_logic.update(green_dispersion, left_motor, right_motor)

            previous_green_detected = green_detected
            
            if red_on_track:
                red_logic.update(left_motor, right_motor)

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