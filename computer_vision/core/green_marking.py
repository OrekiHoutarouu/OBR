import cv2
from computer_vision.core import utils

def get_green_position(green_info, line_info, line_touches_left, line_touches_right, min_green_area=5000):
    """Determine the position of the green marking relative to the detected line.

    Args:
        green_info (dict): A dictionary containing information about the green marking position and orientation.
        line_info (dict): A dictionary containing information about the detected line's position and orientation.
        line_touches_left (bool): Whether the line touches the left edge of the frame.
        line_touches_right (bool): Whether the line touches the right edge of the frame.
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
        green_position["is_on_track"] = True

        if green_info["area"] >= min_green_area:
            if green_info["center_x"] < line_info["center_x"]:
                if line_touches_right and not line_touches_left:
                    green_position["right_of_line"] = True
                else:
                    green_position["left_of_line"] = True
            elif green_info["center_x"] > line_info["center_x"]:
                if line_touches_left and not line_touches_right:
                    green_position["left_of_line"] = True
                else:
                    green_position["right_of_line"] = True

            if green_info["center_y"] < line_info["center_y"]:
                green_position["ahead_of_line"] = True
            else:
                green_position["behind_line"] = True
        else:
            return green_position

    return green_position


def get_green_dispersion(first_largest_green_position, second_largest_green_position, third_largest_green_position, fourth_largest_green_position):
    """Calculate the dispersion of the green markings based on their positions.

    Args:
        first_largest_green_position (dict): Information about the first largest green marking.
        second_largest_green_position (dict): Information about the second largest green marking.
        third_largest_green_position (dict): Information about the third largest green marking.
        fourth_largest_green_position (dict): Information about the fourth largest green marking.

    Returns:
        float: The calculated dispersion of the green markings.
    """  

    dispersion = {
        "top_left": False,
        "top_right": False,
        "bottom_left": False,
        "bottom_right": False
    }

    if not first_largest_green_position["is_on_track"]:
        return dispersion

    for position in [first_largest_green_position, 
                    second_largest_green_position, 
                    third_largest_green_position, 
                    fourth_largest_green_position]:
        
        if position["is_on_track"]:
            if position["left_of_line"] and position["ahead_of_line"]:
                dispersion["top_left"] = True
            elif position["right_of_line"] and position["ahead_of_line"]:
                dispersion["top_right"] = True
            elif position["left_of_line"] and position["behind_line"]:
                dispersion["bottom_left"] = True
            elif position["right_of_line"] and position["behind_line"]:
                dispersion["bottom_right"] = True

    return dispersion