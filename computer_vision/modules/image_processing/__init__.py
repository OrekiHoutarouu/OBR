import cv2

def convert_to_gray(frame):
    """Set the frame to gray scale.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame in gray scale.
    """

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return frame_gray


def blur_frame(frame):
    """Blur the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The blurred frame.
    """

    frame_blur = cv2.GaussianBlur(frame, (5, 5), 0)

    return frame_blur


def set_threshold_black_white(frame):
    """Set the threshold for the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame with threshold applied.
    """

    frame_treshold = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)

    return frame_treshold