from time import sleep

HOLD_STRAIGHT = 2
SPEED = 50

def update(line_info, left_motor, right_motor, max_gap_area=10000):
    """Responds to the line info by controlling the motors to navigate gaps in the line.

    Args:
        line_info (dict): A dictionary containing the line information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
        max_gap_area (int, optional): The maximum area of a gap to consider. Defaults to 10000.
    """

    if line_info["touches_top"] and line_info["touches_bottom"] and line_info["area"] < max_gap_area:
        print("Gap, Go straight")
        
        left_motor.move(SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_STRAIGHT)