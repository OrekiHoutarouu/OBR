def update(distance_sensor):
    """Check whether an object is closer than the minimum safe distance.

    Args:
        distance_sensor (DistanceSensor): The distance sensor object.

    Returns:
        bool: Whether an object is detected within four centimeters.
    """

    distance = distance_sensor.get_distance_cm()

    if distance is None:
        return False
    
    return distance < 15