import cv2

def get_green_center_x(contours, min_area=3000):
    """Gets the center of the green square.

    Args:
        contours (list): A list of contours found in the frame.
        min_area (int): The minimum area of the green square.

    Returns:
        int: The x-coordinate of the green square's center.
    """

    if not contours:
        return 0

    largest_contour = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(largest_contour)
    if area < min_area:
        return 0

    moments = cv2.moments(largest_contour)
    if not moments["m00"]:
        return 0

    green_center_x = int(moments["m10"] / moments["m00"])

    return green_center_x