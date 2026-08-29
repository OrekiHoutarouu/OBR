import platform
import cv2

def get_webcam():
    """Returns the user's main webcam capture object.

    Returns:
        cv2.VideoCapture: The user's main webcam capture object.
    """

    if platform.system() == "Windows":
        capture = cv2.VideoCapture(0)
    else:
        capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    if not capture.isOpened():
        print("Error: Couldn't open webcam.")
        exit()

    capture.set(cv2.CAP_PROP_FPS, 15)
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    return capture


def get_frame(capture):
    """Returns the current frame from the user's webcam.

    Args:
        capture (cv2.VideoCapture): The user's main webcam capture object.

    Returns:
        numpy.ndarray: The current frame from the webcam, or None if unsuccessful.
    """

    success, frame = capture.read()

    if success:
        return frame
    
    return None