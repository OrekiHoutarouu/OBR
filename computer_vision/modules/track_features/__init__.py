from modules import utils
import cv2

def detect_possible_gap(frame, contours): 
    """Detects if there is a possible gap in the line based on the contours found in the frame.

    Args:
        frame (np.ndarray): The input frame.
        contours (list): A list of contours found in the frame.

    Returns:
        bool: True if a possible gap is detected, False otherwise.
    """

    gap_score = 0

    if not contours:
        return False

    if len(contours) > 4:
        gap_score += 1

    top_region = utils.get_roi(frame, "top")
    bottom_region = utils.get_roi(frame, "bottom")

    frame_pixels = cv2.countNonZero(frame)
    top_pixels = cv2.countNonZero(top_region)
    bottom_pixels = cv2.countNonZero(bottom_region)

    if top_pixels < 6000 and bottom_pixels > 6000 or top_pixels > 6000 and bottom_pixels < 6000:
        gap_score += 1

    if frame_pixels < 20000:
        gap_score += 1
    
    return gap_score > 2


def detect_intersection(frame, contours, line_info):
    """Detects if there is an intersection in the line based on the contours found in the frame.

    Args:
        frame (np.ndarray): The input frame.
        contours (list): A list of contours found in the frame.
        line_info (dict): Information about the line.

    Returns:
        bool: True if an intersection is detected, False otherwise.
    """

    intersection_score = 0

    if not contours or not line_info["found"]:
        return False

    if len(contours) < 4:
        intersection_score += 1

    x, y, w, h = cv2.boundingRect(line_info["largest_contour"])
    
    box_area = w * h
    aspect_ratio = w / h
    fill_ratio = line_info["area"] / box_area

    if aspect_ratio > 1.2:
        intersection_score += 1
    
    if fill_ratio < 0.3:
        intersection_score += 1

    return intersection_score > 2


def detect_90_degree_turn():
    pass
