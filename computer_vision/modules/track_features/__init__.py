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

    print(frame_pixels, top_pixels, bottom_pixels)

    if top_pixels < 6000 and bottom_pixels > 6000 or top_pixels > 6000 and bottom_pixels < 6000:
        gap_score += 1

    if frame_pixels < 20000:
        gap_score += 1
    
    return gap_score > 2

def detect_possible_turn_90():
    pass
