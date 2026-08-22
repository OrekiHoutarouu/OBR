from time import sleep

SPEED = 50   
HOLD_FULL_TURN = 6
HOLD_HALF_TURN = 3.5
HOLD_QUARTER_TURN  = 1.5
HOLD_STRAIGHT_LONGER = 0.9
HOLD_STRAIGHT_NORMAL = 0.6
HOLD_STRAIGHT_SHORTER = 0.3
HOLD_IGNORE = 1.5
HOLD_STOP = 0.5

def go_straight_longer(left_motor, right_motor):
    left_motor.move(SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_STRAIGHT_LONGER)


def go_straight_normal(left_motor, right_motor):
    left_motor.move(SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_STRAIGHT_NORMAL)


def go_straight_shorter(left_motor, right_motor):
    left_motor.move(SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_STRAIGHT_SHORTER)


def half_turn_left(left_motor, right_motor):
    left_motor.stop()
    right_motor.stop()

    sleep(HOLD_STOP)

    left_motor.move(SPEED)
    right_motor.move(-SPEED)

    sleep(HOLD_HALF_TURN)


def half_turn_right(left_motor, right_motor):
    left_motor.stop()
    right_motor.stop()

    sleep(HOLD_STOP)

    left_motor.move(-SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_HALF_TURN)


def quarter_turn_right(left_motor, right_motor):
    left_motor.move(SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_STRAIGHT_NORMAL)

    left_motor.stop()
    right_motor.stop()

    sleep(HOLD_STOP)

    left_motor.move(SPEED)
    right_motor.move(-SPEED)

    sleep(HOLD_QUARTER_TURN)

    left_motor.stop()
    right_motor.stop()

    sleep(HOLD_STOP)


def quarter_turn_left(left_motor, right_motor):
    left_motor.move(SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_STRAIGHT_NORMAL)

    left_motor.stop()
    right_motor.stop()

    sleep(HOLD_STOP)

    left_motor.move(-SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_QUARTER_TURN)

    left_motor.stop()
    right_motor.stop()

    sleep(HOLD_STOP)


def ignore(left_motor, right_motor):
    left_motor.move(SPEED)
    right_motor.move(SPEED)

    sleep(HOLD_IGNORE)