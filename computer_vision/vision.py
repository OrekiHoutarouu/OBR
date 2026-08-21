from .core import contours, green_marking, image_processing, utils, webcam
from debug.debug_server import draw_debug_frame
import numpy as np
import cv2
import time

last_frame = None
last_frame_time = time.time()
last_debug_info = {}

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
    
    start = time.perf_counter()
    
    global last_frame
    global last_frame_time
    global last_debug_info
    red_on_track = False

    current_time = time.time()
    fps = 1 / (current_time - last_frame_time)
    fps = round(fps)
    last_frame_time = current_time

    follow_line_roi = image_processing.get_roi(frame, "bottom")
    roi_offset_y = int(frame.shape[0] * 0.4)
    frame_center_x = utils.get_frame_center_x(follow_line_roi)
    webcam_resolution = f"{frame.shape[1]}x{frame.shape[0]}"

    frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    roi_grayscale = cv2.cvtColor(follow_line_roi, cv2.COLOR_BGR2GRAY)
    roi_hsv = roi_hsv = cv2.cvtColor(follow_line_roi, cv2.COLOR_BGR2HSV)
    roi_hsv_clahe = image_processing.get_hsv_clahe(roi_hsv)

    frame_grayscale_blur = cv2.GaussianBlur(frame_grayscale, (5, 5), 0)
    roi_grayscale_blur = cv2.GaussianBlur(roi_grayscale, (5, 5), 0)
    roi_hsv_clahe_blur = cv2.GaussianBlur(roi_hsv_clahe, (5, 5), 0)

    _, frame_black_mask = image_processing.apply_black_mask(frame_grayscale_blur)
    _, roi_black_mask = image_processing.apply_black_mask(roi_grayscale_blur)
    roi_green_mask = image_processing.apply_green_mask(roi_hsv_clahe_blur)
    roi_red_mask = image_processing.apply_red_mask(roi_hsv_clahe_blur)

    roi_black_mask = cv2.bitwise_and(
        roi_black_mask,
        cv2.bitwise_not(
        cv2.bitwise_or(roi_green_mask, roi_red_mask)
        )
    )

    roi_green_mask = cv2.bitwise_and(
        roi_green_mask,
        cv2.bitwise_not(
        cv2.bitwise_or(roi_black_mask, roi_red_mask)
        )
    )

    roi_red_mask = cv2.bitwise_and(
        roi_red_mask,
        cv2.bitwise_not(
        cv2.bitwise_or(roi_black_mask, roi_green_mask)
        )
    ) 

    line_touches_left = bool(np.any(frame_black_mask[:, 0] > 0))
    line_touches_right = bool(np.any(frame_black_mask[:, -1] > 0))
    line_touches_top = bool(np.any(frame_black_mask[0, :] > 0))
    line_touches_bottom = bool(np.any(frame_black_mask[-1, :] > 0))

    line_contours = contours.find_contours(roi_black_mask)
    green_contours = contours.find_contours(roi_green_mask)
    red_contours = contours.find_contours(roi_red_mask)

    largest_green_contours = contours.get_four_largest_contours(green_contours)

    first_largest_green_contour_info = contours.get_contour_info(largest_green_contours[0], frame_center_x)
    second_largest_green_contour_info = contours.get_contour_info(largest_green_contours[1], frame_center_x)
    third_largest_green_contour_info = contours.get_contour_info(largest_green_contours[2], frame_center_x)
    fourth_largest_green_contour_info = contours.get_contour_info(largest_green_contours[3], frame_center_x)

    line_info = contours.get_contour_info(line_contours, frame_center_x)
    line_info.update({
        "touches_left": line_touches_left,
        "touches_right": line_touches_right,
        "touches_top": line_touches_top,
        "touches_bottom": line_touches_bottom
    })

    red_info = contours.get_contour_info(red_contours, frame_center_x)
    if red_info["area"] > 7000:
        red_on_track = True
    
    first_largest_green_position = green_marking.get_green_position(first_largest_green_contour_info, line_info)
    second_largest_green_position = green_marking.get_green_position(second_largest_green_contour_info, line_info)
    third_largest_green_position = green_marking.get_green_position(third_largest_green_contour_info, line_info)
    fourth_largest_green_position = green_marking.get_green_position(fourth_largest_green_contour_info, line_info)

    green_dispersion = green_marking.get_green_dispersion(first_largest_green_position, 
                                                            second_largest_green_position,
                                                            third_largest_green_position,
                                                            fourth_largest_green_position)

    debug_frame = draw_debug_frame(frame, line_contours, line_info, largest_green_contours, red_contours, roi_offset_y)
    last_frame = debug_frame

    debug_info = {
        "current_feature": "Working on it",
        "fps": fps,
        "webcam_resolution": webcam_resolution,
        "latency": round((time.perf_counter() - start) * 1000, 2),
        "line_info": line_info,
        "green_dispersion": green_dispersion,
    }
    last_debug_info = debug_info

    return line_info, green_dispersion, red_on_track