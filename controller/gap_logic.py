HOLD_STRAIGHT = 2.0
SPEED = 20

def update(vision_info, left_motor, right_motor, max_gap_area=10000):
    """Responds to the vision info by controlling the motors to navigate gaps in the line.

    Args:
        vision_info (dict): A dictionary containing the vision information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
        max_gap_area (int, optional): The maximum area of a gap to consider. Defaults to 10000.
    """

    line_info, _ = vision_info

    if line_info["line_info"]["touches_top"] and line_info["line_info"]["touches_bottom"] and line_info["line_info"]["area"] < max_gap_area:
        print("Go straight")
        
        left_motor.move(SPEED, duration=HOLD_STRAIGHT)
        right_motor.move(SPEED, duration=HOLD_STRAIGHT)