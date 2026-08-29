from .core import basic_movements
from time import sleep

def update(green_dispersion, left_motor, right_motor):
    """Responds to the green dispersion info by controlling the motors based on detected green markings.

    Args:
        green_dispersion (dict): A dictionary containing the green dispersion information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
    """

    if green_dispersion["bottom_left"] and green_dispersion["bottom_right"]:
        print("Turn back")
        basic_movements.half_turn_left(left_motor, right_motor)

    elif green_dispersion["bottom_left"]:
        print("Turn left")
        basic_movements.quarter_turn_left(left_motor, right_motor)

    elif green_dispersion["bottom_right"]:
        print("Turn right")
        basic_movements.quarter_turn_right(left_motor, right_motor)

    else:
        print("Ignore")
        basic_movements.ignore(left_motor, right_motor)


def do_second_green_check(capture, vision, left_motor, right_motor):
    """Confirm a green marking across multiple frames before reacting.

    Args:
        capture (cv2.VideoCapture): The webcam capture object.
        vision (module): The vision module used to process each frame.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.

    Returns:
        tuple: (green_detected, confirmed_green_dispersion) where green_detected is a bool
               and confirmed_green_dispersion is the confirmed dispersion dict.
    """

    basic_movements.go_straight_shorter(left_motor, right_motor)
    
    left_motor.stop()
    right_motor.stop()
    
    sleep(2.0)

    GREEN_MARKING_FRAME_COUNT = 10
    green_detection_counts = {
        "top_left": 0,
        "top_right": 0,
        "bottom_left": 0,
        "bottom_right": 0
    }

    for _ in range(GREEN_MARKING_FRAME_COUNT):
        _, current_green_dispersion, _ = vision.update(capture)

        for position, detected in current_green_dispersion.items():
            green_detection_counts[position] += int(detected)

        sleep(0.05)

    minimum_confirmations = GREEN_MARKING_FRAME_COUNT // 2 + 1
    confirmed_green_dispersion = {
        position: count >= minimum_confirmations
        for position, count in green_detection_counts.items()
    }

    green_dispersion = confirmed_green_dispersion
    print(
        f">>> CONFIRMED GREEN: {green_dispersion} "
        f"({green_detection_counts}/{GREEN_MARKING_FRAME_COUNT})"
    )

    green_detected = any(green_dispersion.values())
    
    return green_detected, confirmed_green_dispersion