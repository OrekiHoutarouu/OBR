import cv2, numpy, time

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


def apply_black_mask(frame):
    """Applies a black mask to the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame with the black mask applied.
    """

    frame_black_mask = cv2.threshold(frame, 80, 255, cv2.THRESH_BINARY_INV)

    return frame_black_mask


def apply_green_mask(frame):
    """Applies a green mask to the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The frame with the green mask applied.
    """

    lower_green = numpy.array([40, 80, 40])
    upper_green = numpy.array([96, 255, 255])

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

    lower_red1 = numpy.array([0, 70, 50])
    upper_red1 = numpy.array([10, 255, 255])
    
    lower_red2 = numpy.array([160, 70, 50])
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