from .vehicle_movement import update_vehicle_movement
from .weapon_systems import update_weapon_systems
from .collision_detection import handle_collisions

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
