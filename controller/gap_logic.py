from .core import basic_movements

def update(line_info, left_motor, right_motor):
    """Responds to the line info by controlling the motors to navigate gaps in the line.

    Args:
        line_info (dict): A dictionary containing the line information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
    """

    if not line_info["found"]:
        print("Gap, Go straight")
        basic_movements.go_straight_normal(left_motor, right_motor)