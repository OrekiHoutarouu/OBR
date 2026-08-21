from time import sleep

SPEED = 50   
HOLD_FULL_TURN = 1.6 
HOLD_QUARTER_TURN  = 0.8
HOLD_STRAIGHT = 1
HOLD_IGNORE = 2
HOLD_STOP = 0.5

def update(green_dispersion, left_motor, right_motor):
    """Responds to the green dispersion info by controlling the motors based on detected green markings.

    Args:
        green_dispersion (dict): A dictionary containing the green dispersion information.
        left_motor (TractionModule): The left motor object.
        right_motor (TractionModule): The right motor object.
    """

    if green_dispersion["bottom_left"] and green_dispersion["bottom_right"]:
        print("Turn back")
        
        left_motor.stop()
        right_motor.stop()

        sleep(HOLD_STOP)

        left_motor.move(SPEED)
        right_motor.move(-SPEED)

        sleep(HOLD_FULL_TURN)

    elif green_dispersion["bottom_left"]:
        print("Turn left")

        left_motor.move(SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_STRAIGHT)

        left_motor.stop()
        right_motor.stop()

        sleep(HOLD_STOP)

        left_motor.move(-SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_QUARTER_TURN)

        left_motor.stop()
        right_motor.stop()

        sleep(HOLD_STOP)

        left_motor.move(SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_STRAIGHT)

    elif green_dispersion["bottom_right"]:
        print("Turn right")

        left_motor.move(SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_STRAIGHT)

        left_motor.stop()
        right_motor.stop()

        sleep(HOLD_STOP)

        left_motor.move(SPEED)
        right_motor.move(-SPEED)

        sleep(HOLD_QUARTER_TURN)

        left_motor.stop()
        right_motor.stop()

        sleep(HOLD_STOP)

        left_motor.move(SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_STRAIGHT)

    else:
        print("Ignore")

        left_motor.move(SPEED)
        right_motor.move(SPEED)

        sleep(HOLD_IGNORE)