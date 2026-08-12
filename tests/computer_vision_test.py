from pathlib import Path
from time import sleep
import traceback
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from computer_vision import vision
from computer_vision.core import webcam
from debug.debug_server import start
from computer_vision.core.track_features import get_green_dispersion
from time import sleep

# Run with "python tests/computer_vision_test.py"
# View webcam at "http://localhost:5000/video"

def main():
    capture = webcam.get_webcam()

    start()

    while True:
        try:
            vision_state = vision.update(capture)
            
            if vision_state["first_largest_green_position"]["is_on_track"]:
                green_dispersion = get_green_dispersion(vision_state["first_largest_green_position"], 
                                                        vision_state["second_largest_green_position"],
                                                        vision_state["third_largest_green_position"],
                                                        vision_state["fourth_largest_green_position"])

                print(f"Green dispersion: {green_dispersion}")

        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Stopping execution...")
            
            exit()
        
        except Exception as e:
            tb = e.__traceback__
            error_file, error_line, function, text = traceback.extract_tb(tb)[-1]

            print(f"Error {e} occurred in {error_file} at function {function} at line {error_line}: {text}")
            print("Stopping execution...")
            exit()

if __name__ == "__main__":
    main()