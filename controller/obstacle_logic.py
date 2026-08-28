from .core import basic_movements

def update(left_motor, right_motor):
    """Drive around an obstacle using a predefined movement sequence.

    Args:
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
    """

    basic_movements.quarter_turn_left(left_motor, right_motor)
    basic_movements.go_straight_longer(left_motor, right_motor)
    basic_movements.quarter_turn_right(left_motor, right_motor)
    basic_movements.go_straight_longer(left_motor, right_motor)
    basic_movements.quarter_turn_right(left_motor, right_motor)
    basic_movements.go_straight_longer(left_motor, right_motor)
    basic_movements.quarter_turn_left(left_motor, right_motor)