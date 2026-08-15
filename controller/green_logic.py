from time import sleep

SPEED = 20   
HOLD_TURN  = 1.0 
HOLD_STRAIGHT = 2.0
ANGLE_TURN = 301.7
ANGLE_BACK = 603.4

def update(vision_info, left_motor, right_motor):
    """Responds to the vision info by controlling the motors based on detected green markings.

    Args:
        vision_info (dict): A dictionary containing the vision info information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
    """

    _, green_dispersion = vision_info

    if green_dispersion["bottom_left"] and green_dispersion["bottom_right"]:
        print("Turn back")
        
        left_motor.stop()
        right_motor.stop()

        sleep(0.5)

        left_motor.move_angle(ANGLE_BACK)
        right_motor.move_angle(-ANGLE_BACK)

    elif green_dispersion["bottom_left"]:
        print("Turn left")

        left_motor.move(SPEED, duration=HOLD_TURN)
        right_motor.move(SPEED, duration=HOLD_TURN)

        sleep(0.5)

        left_motor.stop()
        right_motor.stop()

        sleep(0.5)

        left_motor.move_angle(ANGLE_TURN)
        right_motor.move_angle(-ANGLE_TURN)

        sleep(0.5)

        left_motor.stop()
        right_motor.stop()

        sleep(0.5)

        left_motor.move(SPEED, duration=HOLD_TURN)
        right_motor.move(SPEED, duration=HOLD_TURN)

    elif green_dispersion["bottom_right"]:
        print("Turn right")

        left_motor.move(SPEED, duration=HOLD_TURN)
        right_motor.move(SPEED, duration=HOLD_TURN)

        sleep(0.5)

        left_motor.stop()
        right_motor.stop()

        sleep(0.5)

        left_motor.move_angle(-ANGLE_TURN)
        right_motor.move_angle(ANGLE_TURN)

        sleep(0.5)
        
        left_motor.stop()
        right_motor.stop()

        sleep(0.5)
        
        left_motor.move(SPEED, duration=HOLD_TURN)
        right_motor.move(SPEED, duration=HOLD_TURN)

    else:
        print("Go straight")

        left_motor.move(SPEED, duration=HOLD_STRAIGHT)
        right_motor.move(SPEED, duration=HOLD_STRAIGHT)