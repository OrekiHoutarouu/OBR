from .core import basic_movements

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

    elif green_dispersion["bottom_left"] or green_dispersion["top_left"]:
        print("Turn left")
        basic_movements.quarter_turn_left(left_motor, right_motor)

    elif green_dispersion["bottom_right"] or green_dispersion["top_right"]:
        print("Turn right")
        basic_movements.quarter_turn_right(left_motor, right_motor)

    else:
        print("Ignore")
        basic_movements.ignore(left_motor, right_motor)