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


def get_hsv_clahe(frame):
    """Applies CLAHE to the HSV frame.

    Args:
        frame (numpy.ndarray): The input frame in HSV scale.

    Returns:
        numpy.ndarray: The frame with CLAHE applied.
    """

    h, s, v = cv2.split(frame)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    v_clahe = clahe.apply(v)

    frame_hsv_clahe = cv2.merge((h, s, v_clahe))

    return frame_hsv_clahe


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

    frame_black_mask = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

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
    """Applies a red mask to the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame with the green mask applied.
    """

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


def get_roi(frame, region):
    """Get the region of interest (ROI) for following the line.

    Args:
        frame (numpy.ndarray): The input frame.
        region (string): The region of interest.

    Returns:
        numpy.ndarray: The region of interest for following the line.
    """

    height, width = frame.shape[:2]

    if region == "top":
        roi = frame[:int(height * 0.4), :]
    elif region == "bottom":
        roi = frame[int(height * 0.4):, :]

    return roi