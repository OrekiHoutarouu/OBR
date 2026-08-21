from time import sleep

def update(left_motor, right_motor):
    """Responds to the red info by controlling the motors to stop if there is red markings.
    """

    left_motor.move(50)
    right_motor.move(50)

    sleep(1)

    left_motor.stop()
    right_motor.stop()

    sleep(10)