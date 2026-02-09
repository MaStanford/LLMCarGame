import math
from .building_damage import find_building_at, damage_building
from ..data.game_constants import BUILDING_RAM_DAMAGE

def _is_terrain_enterable(terrain):
    """Check if terrain is passable or belongs to an enterable building."""
    if terrain.get("passable", True):
        return True
    building = terrain.get("building", {})
    return building.get("enterable", False)

def update_vehicle_movement(game_state, world, audio_manager, dt):
    """
    Handles the player's vehicle movement, including acceleration, braking, turning, and gas consumption.
    All calculations are now based on delta time (dt) for frame-rate independent physics.
    Returns a list of notification strings.
    """
    notifications = []
    engine_force = 0.0 # Initialize here to ensure it's always available
    
    # --- Vehicle Movement ---
    # Note: Turn rate and acceleration are now defined in units per second.
    turn_this_frame = 0.0
    speed_turn_modifier = max(0.1, 1.0 - (game_state.car_speed / (game_state.max_speed * 1.5 if game_state.max_speed > 0 else 1.5)))
    effective_turn_rate = game_state.turn_rate * speed_turn_modifier
    
    if game_state.actions["turn_right"]: 
        turn_this_frame += effective_turn_rate * dt
    if game_state.actions["turn_left"]: 
        turn_this_frame -= effective_turn_rate * dt
        
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
    if target_speed < 0:
        target_speed *= 0.5 # Reverse speed is capped

    # 2. Calculate the difference between current and target speed
    speed_diff = target_speed - game_state.car_speed

    # 3. Determine the force to apply (acceleration or braking)
    # Use braking_power when decelerating (target speed is closer to zero than current speed),
    # use acceleration_factor when speeding up.
    is_braking = (abs(target_speed) < abs(game_state.car_speed)) or (
        game_state.car_speed > 0 and target_speed < 0) or (
        game_state.car_speed < 0 and target_speed > 0)

    force = game_state.braking_power if is_braking else game_state.acceleration_factor
    change_in_speed = force * math.copysign(1, speed_diff) * dt

    # Prevent overshooting the target speed
    if abs(change_in_speed) > abs(speed_diff):
        change_in_speed = speed_diff

    # 4. Apply coasting resistance if there's no pedal input
    if game_state.pedal_position == 0 and game_state.car_speed != 0:
        drag_force = game_state.drag_coefficient * (game_state.car_speed ** 2) * math.copysign(1, game_state.car_speed)
        friction_force = game_state.friction_coefficient * math.copysign(1, game_state.car_speed)
        change_in_speed -= (drag_force + friction_force) * dt

    # 5. Update car speed
    game_state.car_speed += change_in_speed

    # If braking brought the car to a stop, reset the pedal
    if previous_speed > 0 and game_state.car_speed <= 0 and game_state.pedal_position < 0:
        game_state.car_speed = 0
        game_state.pedal_position = 0.0
    
    # Enforce max speed
    game_state.car_speed = max(-effective_max_speed * 0.5, min(game_state.car_speed, effective_max_speed))

    # Update position based on new velocity
    adjusted_angle = game_state.car_angle - (math.pi / 2)
    game_state.car_velocity_x = game_state.car_speed * math.cos(adjusted_angle)
    game_state.car_velocity_y = game_state.car_speed * math.sin(adjusted_angle)
    
    next_world_x = game_state.car_world_x + game_state.car_velocity_x * dt
    next_world_y = game_state.car_world_y + game_state.car_velocity_y * dt

    # Apply deflection velocity from collisions
    if game_state.deflection_frames > 0:
        next_world_x += game_state.deflection_vx * dt
        next_world_y += game_state.deflection_vy * dt
        game_state.deflection_frames -= 1
        # Decay deflection velocity
        game_state.deflection_vx *= 0.9
        game_state.deflection_vy *= 0.9
        if game_state.deflection_frames <= 0:
            game_state.deflection_vx = 0.0
            game_state.deflection_vy = 0.0
    
    next_center_x = next_world_x + game_state.player_car.width / 2
    next_center_y = next_world_y + game_state.player_car.height / 2
    next_terrain = world.get_terrain_at(next_center_x, next_center_y)

    if _is_terrain_enterable(next_terrain):
        game_state.car_world_x = next_world_x
        game_state.car_world_y = next_world_y
    else:
        # Wall-sliding: try each axis independently so the player slides along walls
        # instead of getting stuck when hitting buildings at an angle.
        dx = next_world_x - game_state.car_world_x
        dy = next_world_y - game_state.car_world_y
        moved = False

        # Try moving in X only
        test_x = game_state.car_world_x + dx
        test_cx = test_x + game_state.player_car.width / 2
        test_cy = game_state.car_world_y + game_state.player_car.height / 2
        terrain_x = world.get_terrain_at(test_cx, test_cy)
        if _is_terrain_enterable(terrain_x):
            game_state.car_world_x = test_x
            moved = True

        # Try moving in Y only
        test_y = game_state.car_world_y + dy
        test_cx = game_state.car_world_x + game_state.player_car.width / 2
        test_cy = test_y + game_state.player_car.height / 2
        terrain_y = world.get_terrain_at(test_cx, test_cy)
        if _is_terrain_enterable(terrain_y):
            game_state.car_world_y = test_y
            moved = True

        if not moved:
            # Fully blocked in both axes - apply collision physics
            audio_manager.play_sfx("crash")
            prev_speed = game_state.car_speed

            # Apply ram damage to buildings
            if "building" in next_terrain:
                ram_damage = max(1, abs(prev_speed) * BUILDING_RAM_DAMAGE)
                city_key, b_idx, b_data = find_building_at(next_center_x, next_center_y)
                if city_key is not None:
                    bld_notes = damage_building(game_state, city_key, b_idx, b_data, ram_damage)
                    notifications.extend(bld_notes)

            if prev_speed < 2.0:
                game_state.car_speed = 0
                game_state.car_velocity_x = 0
                game_state.car_velocity_y = 0
            else:
                game_state.car_speed *= 0.5
                game_state.deflection_vx = -game_state.car_velocity_x * 0.3
                game_state.deflection_vy = -game_state.car_velocity_y * 0.3
                game_state.deflection_frames = 10
            game_state.current_durability -= max(1, int(prev_speed * 0.2)) if not game_state.god_mode else 0
            audio_manager.play_sfx("player_hit")
        elif abs(game_state.car_speed) > 1.0:
            # Sliding along a wall - reduce speed moderately and play a scrape
            game_state.car_speed *= 0.85

    # --- Gas Consumption ---
    distance_this_frame = abs(game_state.car_speed * dt)
    game_state.distance_traveled += distance_this_frame
    gas_used_moving = distance_this_frame * game_state.gas_consumption_rate
    game_state.current_gas = max(0, game_state.current_gas - gas_used_moving)

    # Synchronize the player_car entity's position with the game state
    game_state.player_car.x = game_state.car_world_x
    game_state.player_car.y = game_state.car_world_y

    return notifications

