from .core import image_processing, skeleton, track_features, utils, webcam
import numpy as np
import cv2
import time

last_frame = None

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

    follow_line_roi = image_processing.get_roi(frame, "bottom")
    frame_center_x = utils.get_frame_center_x(follow_line_roi)

    frame_grayscale = image_processing.convert_to_grayscale(follow_line_roi)
    #frame_hsv = image_processing.convert_to_hsv(frame)
    #frame_hsv_clahe = image_processing.get_hsv_clahe(frame_hsv)

    frame_grayscale_blur = image_processing.blur_frame(frame_grayscale)
    #frame_hsv_clahe_blur = image_processing.blur_frame(frame_hsv_clahe)

    _, frame_black_mask = image_processing.apply_black_mask(frame_grayscale_blur)
    #frame_green_mask = image_processing.apply_green_mask(frame_hsv_clahe_blur)
    #frame_red_mask = image_processing.apply_red_mask(frame_hsv_clahe_blur)

    #frame_black_mask = cv2.bitwise_and(
        #frame_black_mask,
        #cv2.bitwise_not(
        #    cv2.bitwise_or(frame_green_mask, frame_red_mask)
        #)
    #)

    #frame_green_mask = cv2.bitwise_and(
    #    frame_green_mask,
    #    cv2.bitwise_not(
    #        cv2.bitwise_or(frame_black_mask, frame_red_mask)
    #    )
    #)

    #frame_red_mask = cv2.bitwise_and(
    #    frame_red_mask,
    #    cv2.bitwise_not(
    #        cv2.bitwise_or(frame_black_mask, frame_green_mask)
    #    )
    #)

    frame_skeleton = skeleton.get_skeleton(frame_black_mask)
    last_frame = frame_skeleton.copy()

    line_contours, _ = utils.find_contours(frame_skeleton)
    #green_contours, _ = utils.find_contours(frame_green_mask)
    #red_contours, _ = utils.find_contours(frame_red_mask)

    line_info = utils.get_contour_info(line_contours, frame_center_x)
    #green_info = utils.get_contour_info(green_contours, frame_center_x)
    #red_info = utils.get_contour_info(red_contours, frame_center_x)

    line_topology = skeleton.get_line_topology(frame_skeleton)
    current_feature = track_features.detect_current_feature(line_info, frame_skeleton)

    return {
        "current_feature": current_feature,
        "skeletonized_frame": frame_skeleton,
        "line_topology": line_topology,
        "line_info": line_info,
        #"green_info": green_info,
        #"red_info": red_info,
    }