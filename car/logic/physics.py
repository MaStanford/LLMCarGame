from .vehicle_movement import update_vehicle_movement
from .weapon_systems import update_weapon_systems
from .collision_detection import handle_collisions
import math

def update_physics_and_collisions(game_state, world, audio_manager):
    """
    Handles all physics updates, weapon systems, and collision detection
    by coordinating calls to specialized modules.
    Returns a list of notification messages.
    """
    # 1. Update player vehicle movement and position
    update_vehicle_movement(game_state, world, audio_manager)

    # 2. Handle weapon firing and projectile updates
    update_weapon_systems(game_state, audio_manager)

    # 3. Update projectile positions and check ranges
    particles_to_keep = []
    for p_state in game_state.active_particles:
        p_x, p_y, p_angle, p_speed, p_power, max_range, p_char, origin_x, origin_y = p_state
        
        # Move projectile
        p_dist = p_speed
        p_x += p_dist * math.cos(p_angle)
        p_y += p_dist * math.sin(p_angle)
        
        # Check range
        distance_traveled = math.sqrt((p_x - origin_x)**2 + (p_y - origin_y)**2)
        
        if distance_traveled < max_range:
            p_state[0], p_state[1] = p_x, p_y
            particles_to_keep.append(p_state)
    game_state.active_particles = particles_to_keep

    # 4. Process all collisions and their effects
    notifications = handle_collisions(game_state, world, audio_manager)

    # 5. Update AI and movement for all non-player entities
    for enemy in game_state.active_enemies:
        enemy.update(game_state, world)
    for fauna in game_state.active_fauna:
        fauna.update(game_state, world)
    for boss in game_state.active_bosses:
        boss.update(game_state, world)
        
    # 6. Despawn entities that are too far away
    despawn_radius_sq = game_state.despawn_radius**2
    game_state.active_enemies = [e for e in game_state.active_enemies if (e.x - game_state.car_world_x)**2 + (e.y - game_state.car_world_y)**2 < despawn_radius_sq]
    game_state.active_fauna = [f for f in game_state.active_fauna if (f.x - game_state.car_world_x)**2 + (f.y - game_state.car_world_y)**2 < despawn_radius_sq]
    game_state.active_obstacles = [o for o in game_state.active_obstacles if (o.x - game_state.car_world_x)**2 + (o.y - game_state.car_world_y)**2 < despawn_radius_sq]
    
    # 7. Check for game over condition
    if game_state.player_car.durability <= 0:
        game_state.game_over = True

    return notifications
