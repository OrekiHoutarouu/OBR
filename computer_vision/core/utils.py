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