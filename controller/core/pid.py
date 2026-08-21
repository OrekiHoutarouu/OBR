from time import time

KP = 0.2
KI = 0
KD = 0.02

integral = 0
previous_error = 0

last_time = time()

def update(error):
    """Calculates the PID correction based on the given error and time delta.

    Args:
        error (int): The error value.
        time_delta (float): The time delta.

    Returns:
        float: The PID correction.
    """

    global integral
    global previous_error
    global last_time

    current_time = time()
    time_delta = current_time - last_time
    last_time = current_time

    integral += error * time_delta

    derivative = 0
    if time_delta > 0:
        derivative = (error - previous_error) / time_delta

    output = (KP * error + KI * integral + KD * derivative)

    previous_error = error

    return output

def reset():
    """Resets variables used in the PID controller."""

    global integral
    global previous_error
    global last_time

    integral = 0
    previous_error = 0
    last_time = time()