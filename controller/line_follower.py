from .core import pid

BASE_SPEED = 20
MAX_SPEED = 100

def update(vision_info, left_motor, right_motor):
    """Updates the motor speeds based on the vision info using a PID controller.

    Args:
        vision_info (dict): The current info of the vision system, including line information and detected features.
        left_motor (TractionModule): Left motor object from the OpenRDK library.
        right_motor (TractionModule): Right motor object from the OpenRDK library.
    """

    error = vision_info["line_info"]["offset_from_frame_center"]
    correction = pid.update(error)

    left_speed = -(BASE_SPEED - correction)
    right_speed = -(BASE_SPEED + correction)

    left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
    right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))

    if vision_info["line_info"]["found"] == True:
        left_motor.move(left_speed)
        right_motor.move(-right_speed)

    else:
        left_motor.stop()
        right_motor.stop()
        pid.reset()