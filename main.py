import traceback
from computer_vision import vision
from computer_vision.core import webcam
from debug.debug_server import start
from controller import line_follower
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

    motor_1 = openrdk.traction(openrdk.get_serial_by_name("left_motor"))
    motor_2 = openrdk.traction(openrdk.get_serial_by_name("right_motor"))

    start()

    while True:
        try:
            vision_state = vision.update(capture)
            line_follower.update(vision_state, motor_1, motor_2)
                
        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Stopping execution...")
            
            motor_1.stop()
            motor_2.stop()
            openrdk.stop()
            
            exit()
        
        except Exception as e:
            tb = e.__traceback__
            error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

            print(f"Error {e} occurred in {error_file} at function {function} at line {error_line}: {text}")
            print("Stopping execution...")
            
            motor_1.stop()
            motor_2.stop()
            openrdk.stop()
            
            exit()


if __name__ == "__main__":
    main()