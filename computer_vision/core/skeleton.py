import cv2
import numpy as np

def get_skeleton(frame_black_mask):
    """Get the skeleton of the track from the black mask frame.

    Args:
        frame_black_mask (np.ndarray): The input black mask frame.

    Returns:
        np.ndarray: The skeleton of the track.
    """

    frame_skeleton = np.zeros(frame_black_mask.shape, np.uint8)

    kernel = cv2.getStructuringElement(
        cv2.MORPH_CROSS,
        (3, 3)
    )

    while True:
        opened = cv2.morphologyEx(frame_black_mask, cv2.MORPH_OPEN, kernel)

        temp = cv2.subtract(frame_black_mask, opened)

        eroded = cv2.erode(frame_black_mask, kernel)

        frame_skeleton = cv2.bitwise_or(frame_skeleton, temp)

        frame_black_mask = eroded.copy()

        if cv2.countNonZero(frame_black_mask) == 0:
            break

    return frame_skeleton