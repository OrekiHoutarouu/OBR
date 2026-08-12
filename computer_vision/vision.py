from .core import image_processing, skeleton, track_features, utils, webcam
from debug.debug_server import draw_debug_frame
import numpy as np
import cv2
import time

last_frame = None
last_frame_time = time.time()

def update(capture):
    """Update the vision state based on the current frame from the webcam.

    Args:
        capture (cv2.VideoCapture): The webcam capture object.

    Returns:
        dict: A dictionary containing the updated vision state.
    """

    frame = webcam.get_frame(capture)
    if frame is None:
        print("No frame captured from webcam.")
        return
    
    global last_frame
    global last_frame_time

    current_time = time.time()
    fps = 1 / (current_time - last_frame_time)
    last_frame_time = current_time

    follow_line_roi = image_processing.get_roi(frame, "bottom")
    roi_offset_y = int(frame.shape[0] * 0.4)
    frame_center_x = utils.get_frame_center_x(follow_line_roi)

    frame_grayscale = cv2.cvtColor(follow_line_roi, cv2.COLOR_BGR2GRAY)
    frame_hsv = frame_hsv = cv2.cvtColor(follow_line_roi, cv2.COLOR_BGR2HSV)
    frame_hsv_clahe = image_processing.get_hsv_clahe(frame_hsv)

    frame_grayscale_blur = cv2.GaussianBlur(frame_grayscale, (5, 5), 0)
    frame_hsv_clahe_blur = cv2.GaussianBlur(frame_hsv_clahe, (5, 5), 0)

    _, frame_black_mask = image_processing.apply_black_mask(frame_grayscale_blur)
    frame_green_mask = image_processing.apply_green_mask(frame_hsv_clahe_blur)
    frame_red_mask = image_processing.apply_red_mask(frame_hsv_clahe_blur)

    frame_black_mask = cv2.bitwise_and(
        frame_black_mask,
        cv2.bitwise_not(
            cv2.bitwise_or(frame_green_mask, frame_red_mask)
        )
    )

    frame_green_mask = cv2.bitwise_and(
        frame_green_mask,
        cv2.bitwise_not(
            cv2.bitwise_or(frame_black_mask, frame_red_mask)
        )
    )

    frame_red_mask = cv2.bitwise_and(
        frame_red_mask,
        cv2.bitwise_not(
            cv2.bitwise_or(frame_black_mask, frame_green_mask)
        )
    )

    frame_skeleton = skeleton.get_skeleton(frame_black_mask)

    line_contours = utils.find_contours(frame_black_mask)
    green_contours = utils.find_contours(frame_green_mask)
    #red_contours, _ = utils.find_contours(frame_red_mask)

    largest_green_contours = utils.get_four_largest_contours(green_contours)

    first_largest_green_contour_info = utils.get_contour_info(largest_green_contours[0], frame_center_x)
    second_largest_green_contour_info = utils.get_contour_info(largest_green_contours[1], frame_center_x)
    third_largest_green_contour_info = utils.get_contour_info(largest_green_contours[2], frame_center_x)
    fourth_largest_green_contour_info = utils.get_contour_info(largest_green_contours[3], frame_center_x)

    line_info = utils.get_contour_info(line_contours, frame_center_x)
    #red_info = utils.get_contour_info(red_contours, frame_center_x)

    line_topology = skeleton.get_line_topology(frame_skeleton)
    debug_frame = draw_debug_frame(frame, line_contours, line_info, largest_green_contours, fps, roi_offset_y)
    last_frame = debug_frame
    
    first_largest_green_position = track_features.get_green_position(first_largest_green_contour_info, line_info)
    second_largest_green_position = track_features.get_green_position(second_largest_green_contour_info, line_info)
    third_largest_green_position = track_features.get_green_position(third_largest_green_contour_info, line_info)
    fourth_largest_green_position = track_features.get_green_position(fourth_largest_green_contour_info, line_info)

    return {
        "skeletonized_frame": frame_skeleton,
        "line_topology": line_topology,
        "line_info": line_info,
        "first_largest_green_contour_info": first_largest_green_contour_info,
        "second_largest_green_contour_info": second_largest_green_contour_info,
        "third_largest_green_contour_info": third_largest_green_contour_info,
        "fourth_largest_green_contour_info": fourth_largest_green_contour_info,
        "first_largest_green_position": first_largest_green_position,
        "second_largest_green_position": second_largest_green_position,
        "third_largest_green_position": third_largest_green_position,
        "fourth_largest_green_position": fourth_largest_green_position,
        #"red_info": red_info,
    }