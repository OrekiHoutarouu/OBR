from .core import pid

BASE_SPEED = 30

def update(vision_state, left_motor, right_motor):
    """Updates the motor speeds based on the vision state using a PID controller.

    Args:
        vision_state (dict): The current state of the vision system, including line information and detected features.
        left_motor (TractionModule): Left motor object from the OpenRDK library.
        right_motor (TractionModule): Right motor object from the OpenRDK library.
    """

    error = vision_state["line_info"]["offset"]
    correction = pid.update(error)

    left_speed = BASE_SPEED + correction
    right_speed = BASE_SPEED - correction

    left_speed = max(-255, min(255, left_speed))
    right_speed = max(-255, min(255, right_speed))

    if vision_state["current_feature"] == "STRAIGHT":
        left_motor.move(left_speed)
        right_motor.move(-right_speed)

    else:
        left_motor.stop()
        right_motor.stop()
        pid.reset()