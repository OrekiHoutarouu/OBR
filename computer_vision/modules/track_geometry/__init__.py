from modules import utils
import cv2

def get_track_info(frame, contours, line_info):
    """Get information about the track based on the frame, contours, and line information.

    Args:
        frame (_type_): The input frame.
        contours (_type_): A list of contours.
        line_info (_type_): A dictionary containing information about the line and its associated contours.

    Returns:
        _type_: A dictionary containing the track information.
    """

    track_info = {
        "contour_count": 0,
        "largest_contour": 0,
        "largest_area": 0,

        "bounding_box": (0, 0, 0, 0),
        "bounding_box_x": 0,
        "bounding_box_y": 0,
        "bounding_box_width": 0,
        "bounding_box_height": 0,

        "aspect_ratio": 0,
        "fill_ratio": 0,

        "line_pixels": 0,
        "top_pixels": 0,
        "bottom_pixels": 0,

        "hull": 0,
        "hull_area": 0,
        "solidity": 0,

        "touches_left_border": False,
        "touches_right_border": False,
        "touches_top_border": False,
        "touches_bottom_border": False
    }
    
    if not line_info["found"]:
        return track_info
    
    track_info["contour_count"] = len(contours)
    track_info["largest_contour"] = line_info["largest_contour"]
    track_info["largest_area"] = line_info["area"]

    track_info["bounding_box"] = get_track_bounding_box(line_info)
    track_info["bounding_box_x"] = track_info["bounding_box"][0]
    track_info["bounding_box_y"] = track_info["bounding_box"][1]
    track_info["bounding_box_width"] = track_info["bounding_box"][2]
    track_info["bounding_box_height"] = track_info["bounding_box"][3]

    track_info["aspect_ratio"] = get_aspect_ratio(track_info["bounding_box_width"], track_info["bounding_box_height"])
    track_info["fill_ratio"] = get_fill_ratio(line_info["area"], track_info["bounding_box_width"], track_info["bounding_box_height"])
    
    track_info["line_pixels"] = cv2.countNonZero(frame)
    track_info["top_pixels"] = get_top_pixels(frame)
    track_info["bottom_pixels"] = get_bottom_pixels(frame)

    track_info["hull"] = cv2.convexHull(line_info["largest_contour"])
    track_info["hull_area"] = cv2.contourArea(track_info["hull"])
    track_info["solidity"] = get_solidity(line_info["area"], track_info["hull_area"])

    track_info["touches_left_border"] = track_info["bounding_box_x"] <= 10
    track_info["touches_right_border"] = track_info["bounding_box_x"] + track_info["bounding_box_width"] >= frame.shape[1] - 10
    track_info["touches_top_border"] = track_info["bounding_box_y"] <= 10
    track_info["touches_bottom_border"] = track_info["bounding_box_y"] + track_info["bounding_box_height"] >= frame.shape[0] - 10

    return track_info


def get_track_bounding_box(line_info):
    """Get the bounding box coordinates of the track.

    Args:
        line_info (dict): A dictionary containing information about the line and its associated contours.

    Returns:
        tuple: The (x, y, w, h) coordinates of the bounding box.
    """

    x, y, w, h = cv2.boundingRect(line_info["largest_contour"])
    
    return x, y, w, h


def get_top_pixels(frame):
    """Get the number of non-zero pixels in the top half of the frame.

    Args:
        frame (np.ndarray): The input frame.

    Returns:
        int: The number of non-zero pixels in the top half of the frame.
    """

    top_region = utils.get_roi(frame, "top")
    top_pixels = cv2.countNonZero(top_region)

    return top_pixels


def get_bottom_pixels(frame):
    """Get the number of non-zero pixels in the bottom half of the frame.

    Args:
        frame (np.ndarray): The input frame.

    Returns:
        int: The number of non-zero pixels in the bottom half of the frame.
    """

    bottom_region = utils.get_roi(frame, "bottom")
    bottom_pixels = cv2.countNonZero(bottom_region)

    return bottom_pixels


def get_fill_ratio(area, bounding_box_width, bounding_box_height):
    """Calculate the fill ratio of the track.

    Args:
        area (float): The area of the track contour.
        bounding_box_width (int): The width of the bounding box.
        bounding_box_height (int): The height of the bounding box.

    Returns:
        float: The fill ratio of the track.
    """

    bounding_box_area = bounding_box_width * bounding_box_height
    fill_ratio = area / bounding_box_area if bounding_box_area != 0 else 0

    return fill_ratio


def get_aspect_ratio(bounding_box_width, bounding_box_height):
    """Calculate the aspect ratio of the track.

    Args:
        bounding_box_width (int): The width of the bounding box.
        bounding_box_height (int): The height of the bounding box.

    Returns:
        float: The aspect ratio of the track.
    """

    aspect_ratio = bounding_box_width / bounding_box_height if bounding_box_height != 0 else 0

    return aspect_ratio


def get_solidity(area, hull_area):
    """Calculate the solidity of the track.

    Args:
        area (float): The area of the track contour.
        hull_area (float): The area of the convex hull of the track contour.

    Returns:
        float: The solidity of the track.
    """

    solidity = area / hull_area if hull_area != 0 else 0

    return solidity