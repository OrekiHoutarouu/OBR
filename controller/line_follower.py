def update(vision_state, motor):
    if vision_state["current_feature"] == "STRAIGHT":
        motor.move(50)  