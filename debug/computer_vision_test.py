from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from computer_vision import vision
from computer_vision.core import webcam
from computer_vision.debug_server import app, start
from time import sleep

# Run with "python debug/computer_vision_test.py"
# View webcam at "http://localhost:5000/video"

def main():
    capture = webcam.get_webcam()

    start()

    while True:
        try:
            vision_state = vision.update(capture)

            print("Line Topology:", vision_state["line_topology"])

        except KeyboardInterrupt:
            print("Stopping execution...")
            
            exit()
        
        except:
            print("An error occurred. Stopping execution...")
            
            exit()

if __name__ == "__main__":
    main()