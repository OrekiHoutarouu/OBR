import cv2, numpy

def convert_to_grayscale(frame):
    """Sets the frame to gray scale.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame in gray scale.
    """

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return frame_gray


def convert_to_hsv(frame):
    """Sets the frame to HSV scale.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame in HSV scale.
    """

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    return frame_hsv


def blur_frame(frame):
    """Blurs the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The blurred frame.
    """

    frame_blur = cv2.GaussianBlur(frame, (5, 5), 0)

    return frame_blur


def apply_black_mask(frame):
    """Applies a black mask to the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame with the black mask applied.
    """

    frame_black_mask = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY_INV)

    return frame_black_mask


def apply_green_mask(frame):
    """Applies a green mask to the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame with the green mask applied.
    """

    lower_green = numpy.array([50, 100, 100])
    upper_green = numpy.array([80, 255, 255])

    frame_green_mask = cv2.inRange(
        frame,
        lower_green,
        upper_green
    )

    return frame_green_mask


def apply_red_mask(frame):
    lower_red1 = numpy.array([0, 120, 150])
    upper_red1 = numpy.array([5, 255, 255])

    lower_red2 = numpy.array([170, 120, 150])
    upper_red2 = numpy.array([180, 255, 255])

    red_mask1 = cv2.inRange(
    frame,
    lower_red1,
    upper_red1
    )

    red_mask2 = cv2.inRange(
        frame,
        lower_red2,
        upper_red2
    )

    red_mask = red_mask1 | red_mask2

    return red_mask