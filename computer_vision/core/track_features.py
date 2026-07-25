import cv2

def get_green_position(green_info, line_info, min_green_area=3000):
    """Determine the position of the green marking relative to the detected line.

    Args:
        green_info (dict): A dictionary containing information about the green marking position and orientation.
        line_info (dict): A dictionary containing information about the detected line's position and orientation.
        min_green_area (int): The minimum area of the green line to be considered valid.

    Returns:
        str: A string indicating the position of the green line relative to the detected line.
    """

    green_position = {
        "is_on_track": False,
        "left_of_line": False,
        "right_of_line": False,
        "ahead_of_line": False,
        "behind_line": False
    }

    if not green_info["found"] or not line_info["found"]:
        return green_position
    
    else:
        green_area = cv2.contourArea(green_info["largest_contour"])
        
        if green_area >= min_green_area:
            if green_info["center_x"] < line_info["center_x"]:
                green_position["left_of_line"] = True
            else:
                green_position["right_of_line"] = True

            if green_info["center_y"] < line_info["center_y"]:
                green_position["ahead_of_line"] = True
            else:
                green_position["behind_line"] = True
        else:
            return

    return green_position
