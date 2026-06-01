import cv2
from modules.utils import get_frame_center_x

def find_contours(frame):
    """Find contours in the frame.

    Args:
        frame (numpy.ndarray): The input frame.

    Returns:
        list: A list of contours found in the frame.
    """

    frame_contours = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return frame_contours


def get_line_center(contours, frame):
    """Get the center of the line.

    Args:
        contours (list): A list of contours found in the frame.
        frame (numpy.ndarray): The input frame.

    Returns:
        int: The x-coordinate of the line's center.
    """

    largest_contour = max(contours, key=cv2.contourArea)
    MOMENT = cv2.moments(largest_contour)

    line_center_x = int(MOMENT["m10"] / MOMENT["m00"])

    return line_center_x