import math

def update_vehicle_movement(game_state, world, audio_manager):
    """
    Handles the player's vehicle movement, including acceleration, braking, turning, and gas consumption.
    """
    # --- Vehicle Movement ---
    turn_this_frame = 0.0
    speed_turn_modifier = max(0.1, 1.0 - (game_state.car_speed / (game_state.max_speed * 1.5 if game_state.max_speed > 0 else 1.5)))
    effective_turn_rate = game_state.turn_rate * speed_turn_modifier
    if game_state.actions["turn_right"]: 
        turn_this_frame += effective_turn_rate
    if game_state.actions["turn_left"]: 
        turn_this_frame -= effective_turn_rate
    game_state.car_angle = (game_state.car_angle + turn_this_frame) % (2 * math.pi)

    current_acceleration_force = 0.0
    current_braking_force = 0.0
    if game_state.actions["accelerate"] and game_state.current_gas > 0: 
        current_acceleration_force = game_state.acceleration_factor
    if game_state.actions["brake"]: 
        current_braking_force = game_state.braking_power
    
    drag_force = (game_state.drag_coefficient * (game_state.car_speed**2)) + 0.005
    speed_change = current_acceleration_force - drag_force - current_braking_force
    game_state.car_speed += speed_change

    car_center_world_x = game_state.car_world_x + game_state.player_car.width / 2
    car_center_world_y = game_state.car_world_y + game_state.player_car.height / 2
    current_terrain = world.get_terrain_at(car_center_world_x, car_center_world_y)
    terrain_speed_mod = current_terrain.get("speed_modifier", 1.0)
    effective_max_speed = game_state.max_speed * terrain_speed_mod
    game_state.car_speed = max(0, min(game_state.car_speed, effective_max_speed if effective_max_speed > 0 else 0))

    game_state.car_velocity_x = game_state.car_speed * math.cos(game_state.car_angle)
    game_state.car_velocity_y = game_state.car_speed * math.sin(game_state.car_angle)
    next_world_x = game_state.car_world_x + game_state.car_velocity_x
    next_world_y = game_state.car_world_y + game_state.car_velocity_y
    next_center_x = next_world_x + game_state.player_car.width / 2
    next_center_y = next_world_y + game_state.player_car.height / 2
    next_terrain = world.get_terrain_at(next_center_x, next_center_y)
    if next_terrain.get("passable", True):
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
    gas_used_accel = current_acceleration_force * 0.1 if current_acceleration_force > 0 else 0
    game_state.current_gas = max(0, game_state.current_gas - (gas_used_moving + gas_used_accel))
