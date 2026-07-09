import cv2
import numpy as np

def get_skeleton(frame_black_mask):
    """Get the skeleton of the line from the black mask frame.

    Args:
        frame_black_mask (np.ndarray): The input black mask frame.

    Returns:
        np.ndarray: The skeleton of the line.
    """

    frame_black_mask = (frame_black_mask > 0).astype(np.uint8) * 255
    frame_skeleton = cv2.ximgproc.thinning(frame_black_mask)

    return frame_skeleton


def get_line_topology(skeleton):
    """Get the track topology from the skeleton of the line.

    Args:
        skeleton (np.ndarray): The input skeleton frame.

    Returns:
        dict: A dictionary containing the endpoints and junctions of the track.
    """

    line_topology = {
        "endpoints": find_endpoints(skeleton),
        "junctions": find_junctions(skeleton)
    }

    return line_topology


def get_neighbor_count(skeleton):
    """Get the number of neighbors for each pixel in the skeleton.

    Args:
        skeleton (np.ndarray): The input skeleton frame.

    Returns:
        np.ndarray: An array containing the number of neighbors for each pixel.
    """

    skeleton = (skeleton > 0).astype(np.uint8)

    kernel = np.array([
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ], dtype=np.uint8)

    return cv2.filter2D(skeleton, -1, kernel)


def find_endpoints(skeleton):
    """Find the endpoints of the skeleton.

    Args:
        skeleton (np.ndarray): The input skeleton frame.

    Returns:
        list: A list of endpoints as (x, y) coordinates.
    """

    neighbors = get_neighbor_count(skeleton)

    endpoints = np.logical_and(
        skeleton > 0,
        neighbors == 1
    )

    num_labels, _ = cv2.connectedComponents(
        endpoints.astype(np.uint8)
    )

    return num_labels - 1


def find_junctions(skeleton):
    """Find the junctions of the skeleton.

    Args:
        skeleton (np.ndarray): The input skeleton frame.

    Returns:
        list: A list of junctions as (x, y) coordinates.
    """

    neighbors = get_neighbor_count(skeleton)

    junctions = np.logical_and(
        skeleton > 0,
        neighbors >= 3
    )

    num_labels, _ = cv2.connectedComponents(
        junctions.astype(np.uint8)
    )

    return num_labels - 1