from .vehicle_movement import update_vehicle_movement
from .weapon_systems import update_weapon_systems
from .collision_detection import handle_collisions
import logging
import math

def update_physics_and_collisions(game_state, world, audio_manager, stdscr, color_pair_map):
    """
    Handles all physics updates, weapon systems, and collision detection
    by coordinating calls to specialized modules.
    """
    # 1. Update player vehicle movement and position
    update_vehicle_movement(game_state, world, audio_manager)

    # 2. Handle weapon firing and projectile updates
    update_weapon_systems(game_state, audio_manager)

    # 3. Process all collisions and their effects
    handle_collisions(game_state, world, audio_manager, stdscr, color_pair_map)

    # 4. Update enemy AI and movement
    for enemy in game_state.active_enemies:
        enemy.update(game_state, world)
        
    # 5. Despawn entities that are too far away
    game_state.active_enemies = [e for e in game_state.active_enemies if (e.x - game_state.car_world_x)**2 + (e.y - game_state.car_world_y)**2 < game_state.despawn_radius**2]
    game_state.active_fauna = [f for f in game_state.active_fauna if (f.x - game_state.car_world_x)**2 + (f.y - game_state.car_world_y)**2 < game_state.despawn_radius**2]
    game_state.active_obstacles = [o for o in game_state.active_obstacles if (o.x - game_state.car_world_x)**2 + (o.y - game_state.car_world_y)**2 < game_state.despawn_radius**2]
    
    # 6. Update projectiles
    particles_to_remove = []
    for i, p_state in enumerate(game_state.active_particles):
        p_x, p_y, p_angle, p_speed, p_power, p_range_left, p_char = p_state
        
        p_dist = p_speed
        p_x += p_dist * math.cos(p_angle)
        p_y += p_dist * math.sin(p_angle)
        p_range_left -= p_dist
        
        if p_range_left <= 0:
            particles_to_remove.append(i)
        else:
            game_state.active_particles[i] = [p_x, p_y, p_angle, p_speed, p_power, p_range_left, p_char]
            logging.info(f"PHYSICS: Updating projectile {i} to ({p_x:.2f}, {p_y:.2f})")

    for i in sorted(particles_to_remove, reverse=True):
        del game_state.active_particles[i]
