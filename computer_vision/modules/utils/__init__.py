def get_frame_center_x(frame):
    height, width = frame.shape[:2]

    frame_center_x = width // 2

    return frame_center_x


def get_offset(setpoint, measured_value):
    offset = setpoint - measured_value

    return offset