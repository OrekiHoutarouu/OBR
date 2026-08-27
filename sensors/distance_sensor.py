def update(distance_sensor):
    distance = distance_sensor.get_distance_cm()

    if distance is None:
        return False
    
    return distance < 4