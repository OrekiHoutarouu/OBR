import cv2

def get_webcam():
    """Returns the user's main webcam capture object.

    Returns:
        cv2.VideoCapture: The user's main webcam capture object.
    """
    
    capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)

    if not capture.isOpened():
        exit()

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