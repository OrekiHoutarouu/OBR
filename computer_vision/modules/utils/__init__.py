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


def get_contour_info(contours, frame_center_x, min_area):
    """Get information about the line based on the contours found in the frame.

    Args:
        contours (list): A list of contours found in the frame.
        frame_center_x (int): The x-coordinate of the frame's center.
        min_area (int, optional): The minimum area for a contour to be considered a line. Defaults to 15000.

    Returns:
        dict: A dictionary containing information about the detected line.
    """

    contour_info = {
        "found": False,
        "largest_contour": 0,
        "area": 0,
        "center_x": 0,
        "offset": 0
    }

    if not contours:
        return contour_info
    
    largest_contour = max(contours, key=cv2.contourArea)
    
    area = cv2.contourArea(largest_contour)
    if area < min_area:
        return contour_info
    
    moments = cv2.moments(largest_contour)
    if not moments["m00"]:
        return contour_info
    
    contour_info["found"] = True
    contour_info["largest_contour"] = largest_contour
    contour_info["area"] = area
    contour_info["center_x"] = get_contour_center_x(moments)
    contour_info["offset"] = get_offset(frame_center_x, contour_info["center_x"])

    return contour_info


def get_contour_center_x(moments):
    """Get the x-coordinate of the line's center based on the moments of the contour.

    Args:
        moments (dict): A dictionary containing the moments of the contour.

    Returns:
        int: The x-coordinate of the line's center.
    """

    line_center_x = int(moments["m10"] / moments["m00"])

    return line_center_x


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