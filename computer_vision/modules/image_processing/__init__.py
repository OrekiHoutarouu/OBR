import cv2

def convert_to_gray(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return frame_gray


def blur_frame(frame):
    frame_blur = cv2.GaussianBlur(frame, (5, 5), 0)

    return frame_blur


def set_threshold(frame):
    frame_treshold = cv2.threshold(frame, 80, 255, cv2.THRESH_BINARY_INV)

    return frame_treshold


def find_contours(frame):
    frame_contours = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return frame_contours