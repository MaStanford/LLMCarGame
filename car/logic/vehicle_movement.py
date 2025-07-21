import math

def update_vehicle_movement(game_state, world, audio_manager):
    """
    Handles the player's vehicle movement, including acceleration, braking, turning, and gas consumption.
    """
    engine_force = 0.0 # Initialize here to ensure it's always available
    # --- Vehicle Movement ---
    turn_this_frame = 0.0
    speed_turn_modifier = max(0.1, 1.0 - (game_state.car_speed / (game_state.max_speed * 1.5 if game_state.max_speed > 0 else 1.5)))
    effective_turn_rate = game_state.turn_rate * speed_turn_modifier
    if game_state.actions["turn_right"]: 
        turn_this_frame += effective_turn_rate
    if game_state.actions["turn_left"]: 
        turn_this_frame -= effective_turn_rate
    game_state.car_angle = (game_state.car_angle + turn_this_frame) % (2 * math.pi)
    game_state.player_car.angle = game_state.car_angle

    # Store speed before physics calculations
    previous_speed = game_state.car_speed

    # --- Terrain and Speed Limits ---
    car_center_world_x = game_state.car_world_x + game_state.player_car.width / 2
    car_center_world_y = game_state.car_world_y + game_state.player_car.height / 2
    current_terrain = world.get_terrain_at(car_center_world_x, car_center_world_y)
    terrain_speed_mod = current_terrain.get("speed_modifier", 1.0)
    effective_max_speed = game_state.max_speed * terrain_speed_mod

    # --- Physics Calculations ---
    # 1. Calculate target speed based on pedal position
    target_speed = game_state.pedal_position * effective_max_speed
    # Reverse speed is capped at 50% of max speed
    if target_speed < 0:
        target_speed *= 0.5

    # 2. Calculate the difference between current and target speed
    speed_diff = target_speed - game_state.car_speed

    # 3. Determine the force to apply (acceleration or braking)
    # The force is proportional to the car's acceleration stat, but we ensure it doesn't overshoot the target.
    if abs(speed_diff) < game_state.acceleration_factor:
        change_in_speed = speed_diff
    else:
        change_in_speed = game_state.acceleration_factor * math.copysign(1, speed_diff)

    # 4. Apply coasting resistance if there's no pedal input
    if game_state.pedal_position == 0:
        drag_force = game_state.drag_coefficient * (game_state.car_speed ** 2) * math.copysign(1, game_state.car_speed)
        friction_force = game_state.friction_coefficient * math.copysign(1, game_state.car_speed) if game_state.car_speed != 0 else 0
        change_in_speed -= (drag_force + friction_force)

    # 5. Update car speed
    game_state.car_speed += change_in_speed

    # If braking brought the car to a stop, reset the pedal to prevent instant reverse
    if previous_speed > 0 and game_state.car_speed <= 0 and game_state.pedal_position < 0:
        game_state.car_speed = 0
        game_state.pedal_position = 0.0
    
    # Enforce max speed (and max reverse speed)
    game_state.car_speed = max(-effective_max_speed * 0.5, min(game_state.car_speed, effective_max_speed))

    # Adjust angle for world coordinates (0 is North, but math functions treat 0 as East)
    adjusted_angle = game_state.car_angle - (math.pi / 2)
    game_state.car_velocity_x = game_state.car_speed * math.cos(adjusted_angle)
    game_state.car_velocity_y = game_state.car_speed * math.sin(adjusted_angle)
    next_world_x = game_state.car_world_x + game_state.car_velocity_x
    next_world_y = game_state.car_world_y + game_state.car_velocity_y
    next_center_x = next_world_x + game_state.player_car.width / 2
    next_center_y = next_world_y + game_state.player_car.height / 2
    next_terrain = world.get_terrain_at(next_center_x, next_center_y)
    
    is_shop = next_terrain.get("building", {}).get("shop_type") is not None
    
    if next_terrain.get("passable", True) or is_shop:
        game_state.car_world_x = next_world_x
        game_state.car_world_y = next_world_y
    else:
        audio_manager.play_sfx("crash")
        prev_speed = game_state.car_speed
        game_state.car_speed = 0
        game_state.car_velocity_x = 0
        game_state.car_velocity_y = 0
        game_state.current_durability -= max(1, int(prev_speed * 2))
        audio_manager.play_sfx("player_hit")


    distance_this_frame = game_state.car_speed
    game_state.distance_traveled += distance_this_frame
    gas_used_moving = distance_this_frame * game_state.gas_consumption_rate * game_state.gas_consumption_scaler
    gas_used_accel = engine_force * 0.1 if engine_force > 0 else 0
    game_state.current_gas = max(0, game_state.current_gas - (gas_used_moving + gas_used_accel))

    # Synchronize the player_car entity's position with the game state
    game_state.player_car.x = game_state.car_world_x
    game_state.player_car.y = game_state.car_world_y

