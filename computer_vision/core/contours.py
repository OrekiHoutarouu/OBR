from .utils import get_offset
import cv2
import numpy as np

def find_contours(frame):
    """Find contours in the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        list: A list of contours found in the frame.
    """

    frame_contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return frame_contours


def get_four_largest_contours(contours):
    """Get the four largest contours from the list of contours.

    Args:
        contours (list): A list of contours found in the frame.

    Returns:
        list: A list containing the four largest contours.
    """

    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

    largest_contours += [0] * (4 - len(largest_contours))

    return largest_contours


def get_contour_info(contours, frame_center_x):
    """Get information about the line based on one or more contours.

    Args:
        contours (list or numpy.ndarray): A list of contours, a single contour, or None.
        frame_center_x (int): The x-coordinate of the frame's center.

    Returns:
        dict: A dictionary containing information about the detected line.
    """

    contour_info = {
        "found": False,
        "center_x": 0,
        "center_y": 0,
        "area": 0,
        "offset_from_frame_center": 0
    }

    if contours is None:
        return contour_info

    if isinstance(contours, (list, tuple)):
        contour_list = [c for c in contours if c is not None and hasattr(c, "shape")]
    elif hasattr(contours, "shape"):
        contour_list = [contours]
    else:
        return contour_info

    if not contour_list:
        return contour_info

    largest_contour = max(contour_list, key=cv2.contourArea)
    
    moments = cv2.moments(largest_contour)
    if not moments["m00"]:
        return contour_info
    
    contour_info["found"] = True
    contour_info["center_x"] = get_contour_center_x(moments)
    contour_info["center_y"] = get_contour_center_y(moments)
    contour_info["area"] = cv2.contourArea(largest_contour)
    contour_info["offset_from_frame_center"] = get_offset(frame_center_x, contour_info["center_x"])

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


def get_contour_center_y(moments):
    """Get the y-coordinate of the line's center based on the moments of the contour.

    Args:
        moments (dict): A dictionary containing the moments of the contour.

    Returns:
        int: The y-coordinate of the line's center.
    """

    line_center_y = int(moments["m01"] / moments["m00"])

    return line_center_y