import cv2

def find_contours(frame):
    frame_contours = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return frame_contours