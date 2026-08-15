import traceback
from computer_vision import vision
from computer_vision.core import webcam
from controller import green_logic, line_follower
from debug.debug_server import start
from open_rdk import CommsRuntime
from time import sleep

# Run with "PYTHONPATH=open_rdk/host/main/src python3 main.py"
# View webcam at "http://localhost:5000/video"

def main():
    capture = webcam.get_webcam()
    openrdk = CommsRuntime(auto_start=True, enable_webview=True, enable_webview_updates=True)

    sleep(2)

    openrdk.list_devices(verbose=True)
    openrdk.post("webview_complete")

    left_motor = openrdk.traction(openrdk.get_serial_by_name("left_motor"))
    right_motor = openrdk.traction(openrdk.get_serial_by_name("right_motor"))

    start()

    while True:
        try:
            vision_state = vision.update(capture)
            line_follower.update(vision_state, left_motor, right_motor)
            green_logic.update(vision_state, left_motor, right_motor)

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