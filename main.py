from computer_vision import vision
from computer_vision.core import webcam
from computer_vision.debug_server import app, start
from controller import line_follower
from openrdk import CommsRuntime
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
            print("Stopping execution...")
            
            motor_1.stop()
            motor_2.stop()
            openrdk.stop()
            
            exit()
        
        except:
            print("An error occurred. Stopping execution...")
            
            motor_1.stop()
            motor_2.stop()
            openrdk.stop()
            
            exit()

if __name__ == "__main__":
    main()