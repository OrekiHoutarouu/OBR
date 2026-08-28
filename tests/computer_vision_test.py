from pathlib import Path
import traceback
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from computer_vision import vision
from computer_vision.core import webcam
from controller import green_logic
from debug.debug_server import start

# Run with "python tests/computer_vision_test.py"
# View webcam at "http://localhost:5000"

def main():
    """Start webcam vision processing and the debug web server."""

    capture = webcam.get_webcam()

    start()

    while True:
        try:
            vision_info = vision.update(capture, debug=True)

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