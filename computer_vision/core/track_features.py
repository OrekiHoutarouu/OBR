def detect_current_feature(track_info, line_info, frame):
    """Detect the current feature of the track based on the track information and line information.

    Args:
        track_info (dict): A dictionary containing information about the track.
        line_info (dict): A dictionary containing information about the line.

    Returns:
        str: The detected feature of the track.
    """

    if not line_info["found"]:
        return "GAP"

    if (track_info["aspect_ratio"] < 0.3 and track_info["fill_ratio"] > 0.6):
        return "STRAIGHT"

    if (track_info["touches_left_border"] and track_info["touches_right_border"]):
        if track_info["touches_top_border"]:
            return "CROSS"
        
        return "T"

    if (track_info["aspect_ratio"] > 0.6 and not track_info["touches_top_border"] and track_info["touches_bottom_border"]):
        if track_info["touches_left_border"]:
            return "TURN_90_LEFT"
        if track_info["touches_right_border"]:  
            return "TURN_90_RIGHT"

    return "UNKNOWN"