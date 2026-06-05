from modules import utils
import cv2

def get_line_info(contours, frame_center_x, min_area=15000):
    """Get information about the line based on the contours found in the frame.

    Args:
        contours (list): A list of contours found in the frame.
        frame_center_x (int): The x-coordinate of the frame's center.
        min_area (int, optional): The minimum area for a contour to be considered a line. Defaults to 15000.

    Returns:
        dict: A dictionary containing information about the detected line.
    """

    line_info = {
        "found": False,
        "largest_contour": 0,
        "area": 0,
        "center_x": 0,
        "offset": 0
    }

    if not contours:
        return line_info
    
    largest_contour = max(contours, key=cv2.contourArea)
    
    area = cv2.contourArea(largest_contour)
    if area < min_area:
        return line_info
    
    moments = cv2.moments(largest_contour)
    if not moments["m00"]:
        return line_info
    
    line_info["found"] = True
    line_info["largest_contour"] = largest_contour
    line_info["area"] = area
    line_info["center_x"] = get_line_center_x(moments)
    line_info["offset"] = utils.get_offset(frame_center_x, line_info["center_x"])

    return line_info


def get_line_center_x(moments):
    """Get the x-coordinate of the line's center based on the moments of the contour.

    Args:
        moments (dict): A dictionary containing the moments of the contour.

    Returns:
        int: The x-coordinate of the line's center.
    """

    line_center_x = int(moments["m10"] / moments["m00"])

    return line_center_x
