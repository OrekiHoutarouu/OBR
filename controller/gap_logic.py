from .core import basic_movements

def update(line_info, left_motor, right_motor, max_gap_area=10000):
    """Responds to the line info by controlling the motors to navigate gaps in the line.

    Args:
        line_info (dict): A dictionary containing the line information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
        max_gap_area (int, optional): The maximum area of a gap to consider. Defaults to 10000.
    """

    if not line_info["found"]:
        print("Gap, Go straight")
        basic_movements.go_straight_normal(left_motor, right_motor)