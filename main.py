from computer_vision.vision import update
from computer_vision.modules import webcam
from openrdk import CommsRuntime
from time import sleep

# PYTHONPATH=open_rdk/host/main/src python3 main.py

def main():
    capture = webcam.get_webcam()
    #openrdk = CommsRuntime(auto_start=True, enable_webview=False, enable_webview_updates=False)
    
    #sleep(2)

    #openrdk.list_devices(verbose=True)
    #motor = openrdk.traction(openrdk.get_serial_by_name("motor_samuel"))

    while True:
        vision_state = update(capture)

        print(vision_state["current_feature"])

if __name__ == "__main__":
    main()