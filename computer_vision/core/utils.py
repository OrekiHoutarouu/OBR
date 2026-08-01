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


def get_contour_info(contours, frame_center_x):
    """Get information about the line based on the contours found in the frame.

    Args:
        contours (list): A list of contours found in the frame.
        frame_center_x (int): The x-coordinate of the frame's center.

    Returns:
        dict: A dictionary containing information about the detected line.
    """

    contour_info = {
        "found": False,
        "largest_contours": 0,
        "center_x": 0,
        "center_y": 0,
        "offset": 0
    }

    if not contours:
        return contour_info
    
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
    
    moments = cv2.moments(largest_contours[0])
    if not moments["m00"]:
        return contour_info
    
    contour_info["found"] = True
    contour_info["largest_contours"] = largest_contours
    contour_info["center_x"] = get_contour_center_x(moments)
    contour_info["center_y"] = get_contour_center_y(moments)
    contour_info["offset"] = get_offset(frame_center_x, contour_info["center_x"])

    return contour_info


def get_largest_contour_areas(contours):
    largest_green_area = (
        cv2.contourArea(contours[0])
        if len(contours) > 0
        and contours[0] is not None
        else 0
    )
    second_largest_green_area = (
        cv2.contourArea(contours[1])
        if len(contours) > 1
        and contours[1] is not None
        else 0
    )
    third_largest_green_area = (
        cv2.contourArea(contours[2])
        if len(contours) > 2
        and contours[2] is not None
        else 0
    )
    fourth_largest_green_area = (
        cv2.contourArea(contours[3])
        if len(contours) > 3
        and contours[3] is not None
        else 0
    )

    return largest_green_area, second_largest_green_area, third_largest_green_area, fourth_largest_green_area


def get_contour_center_x(moments):
    """Get the x-coordinate of the line's center based on the moments of the contour.

    Args:
        moments (dict): A dictionary containing the moments of the contour.

    Returns:
        int: The x-coordinate of the line's center.
    """

    line_center_x = int(moments["m10"] / moments["m00"])

    return line_center_x


def get_contour_center_y(moments):
    """Get the y-coordinate of the line's center based on the moments of the contour.

    Args:
        moments (dict): A dictionary containing the moments of the contour.

    Returns:
        int: The y-coordinate of the line's center.
    """

    line_center_y = int(moments["m01"] / moments["m00"])

    return line_center_y


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