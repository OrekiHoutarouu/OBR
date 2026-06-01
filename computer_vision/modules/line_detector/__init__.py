import cv2

def get_line_center(contours):
    """Get the center of the line.

    Args:
        contours (list): A list of contours found in the frame.
        frame (numpy.ndarray): The input frame.

    Returns:
        int: The x-coordinate of the line's center.
    """

    largest_contour = max(contours, key=cv2.contourArea)
    moments = cv2.moments(largest_contour)

    line_center_x = int(moments["m10"] / moments["m00"])

    return line_center_x