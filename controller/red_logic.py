from .core import basic_movements
from time import sleep

def update(left_motor, right_motor):
    """Responds to the red info by controlling the motors to stop if there is red markings.

    Args:
        left_motor (TractionModule): Left motor object from the OpenRDK library.
        right_motor (TractionModule): Right motor object from the OpenRDK library.
    """

    basic_movements.go_straight_normal(left_motor, right_motor)

    left_motor.stop()
    right_motor.stop()

    raise Exception("The robot reached the end of the track!")