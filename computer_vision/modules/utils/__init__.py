import cv2

def find_contours(frame):
    """Find contours in the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        list: A list of contours found in the frame.
    """

    frame_contours = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return frame_contours


def get_frame_center_x(frame):
    """Get the x-coordinate of the center of the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        int: The x-coordinate of the center of the frame.
    """

    height, width = frame.shape[:2]

    frame_center_x = width // 2

    return frame_center_x


def get_roi(frame, region):
    """Get the region of interest (ROI) for following the line.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        numpy.ndarray: The region of interest for following the line.
    """

    height, width = frame.shape

    if region == "top":
        roi = frame[:height//2, :]
    elif region == "bottom":
        roi = frame[height//2:, :]

    return roi


def get_offset(setpoint, measured_value):
    """Get the offset between the setpoint and the measured value.

    Args:
        setpoint (int): The desired position.
        measured_value (int): The actual position.

    Returns:
        int: The offset between the setpoint and the measured value.
    """

    offset = setpoint - measured_value

    return offset