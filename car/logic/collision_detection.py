import random
import math
from .loot_generation import handle_enemy_loot_drop
from ..world.generation import get_buildings_in_city

def find_safe_exit_spot(world, building):
    """
    Finds a safe, non-colliding spot to place the player after exiting a building.
    It checks in a spiral pattern around the building's center.
    """
    center_x, center_y = building['x'] + building['w'] // 2, building['y'] + building['h'] // 2
    
    # Spiral search
    x, y = 0, 0
    dx, dy = 0, -1
    max_dist = max(building['w'], building['h']) * 2 # Search a reasonable area
    
    for _ in range(max_dist**2):
        check_x, check_y = center_x + x, center_y + y
        terrain = world.get_terrain_at(check_x, check_y)
        
        # Check if the spot is passable and not inside any building
        if terrain.get("passable", True) and not any(
            b['x'] <= check_x < b['x'] + b['w'] and b['y'] <= check_y < b['y'] + b['h']
            for b in get_buildings_in_city(round(check_x / 1000), round(check_y / 1000))
        ):
            return check_x, check_y
            
        if x == y or (x < 0 and x == -y) or (x > 0 and x == 1 - y):
            dx, dy = -dy, dx
        x, y = x + dx, y + dy
        
    return building['x'], building['y'] # Fallback

def check_collision(rect1, rect2):
    """Checks if two rectangles are colliding."""
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

def handle_collisions(game_state, world, audio_manager):
    """
    Handles all collision detection and resolution.
    Returns a list of notification messages.
    """
    notifications = []
    
    # --- Projectile Collisions ---
    projectiles_to_remove = set()
    
    # Using a copy of the list to iterate while potentially modifying the original
    for i, p_state in enumerate(game_state.active_particles):
        p_x, p_y, _, _, p_power, _, _, _, _ = p_state
        
        # Check for collisions with terrain
        p_terrain = world.get_terrain_at(p_x, p_y)
        if not p_terrain.get("passable", True):
            projectiles_to_remove.add(i)
            continue

        # Check for collisions with enemies
        for enemy in game_state.active_enemies:
            if (enemy.x <= p_x < enemy.x + enemy.width and 
                enemy.y <= p_y < enemy.y + enemy.height):
                enemy.durability -= p_power
                audio_manager.play_sfx("enemy_hit")
                projectiles_to_remove.add(i)
                if enemy.durability <= 0:
                    game_state.destroyed_this_frame.append(enemy)
                    handle_enemy_loot_drop(game_state, enemy)
                    notifications.append(f"Destroyed {enemy.__class__.__name__}!")
                    game_state.active_enemies.remove(enemy)
                break # Projectile can only hit one enemy
        
    # Remove projectiles that have collided
    if projectiles_to_remove:
        game_state.active_particles = [p for i, p in enumerate(game_state.active_particles) if i not in projectiles_to_remove]

    # --- Player-Enemy Collision ---
    player = game_state.player_car
    player_rect = (player.x, player.y, player.width, player.height)
    
    for enemy in game_state.active_enemies[:]: # Iterate over a copy
        enemy_rect = (enemy.x, enemy.y, enemy.width, enemy.height)
        if check_collision(player_rect, enemy_rect):
            audio_manager.play_sfx("crash")
            
            # Apply damage (assuming enemies have a collision_damage attribute)
            game_state.current_durability -= getattr(enemy, "collision_damage", 5)
            enemy.durability -= getattr(player, "collision_damage", 5)
            
            if enemy.durability <= 0:
                game_state.destroyed_this_frame.append(enemy)
                handle_enemy_loot_drop(game_state, enemy)
                notifications.append(f"Destroyed {enemy.__class__.__name__}!")
                game_state.active_enemies.remove(enemy)

    # --- Obstacle Collisions ---
    for obstacle in game_state.active_obstacles[:]: # Iterate over a copy
        obstacle_rect = (obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        if check_collision(player_rect, obstacle_rect):
            
            audio_manager.play_sfx("crash")
            game_state.current_durability -= obstacle.damage
            obstacle.durability -= 10
            if obstacle.durability <= 0:
                game_state.active_obstacles.remove(obstacle)
                game_state.gain_xp(obstacle.xp_value)
                if random.random() < obstacle.drop_rate:
                    pass # Future loot drop implementation

    # --- Pickup Collisions ---
    pickups_to_remove = []
    for pickup_id, pickup in game_state.active_pickups.items():
        if (game_state.player_car.x < pickup["x"] + 1 and
            game_state.player_car.x + game_state.player_car.width > pickup["x"] and
            game_state.player_car.y < pickup["y"] + 1 and
            game_state.player_car.y + game_state.player_car.height > pickup["y"]):
            
            if pickup["type"] == "cash":
                game_state.player_cash += pickup["value"]
                notifications.append(f"Picked up {pickup['value']} cash!")
            elif pickup["type"] == "weapon":
                game_state.player_inventory.append(pickup["weapon"])
                notifications.append(f"Picked up {pickup['weapon'].name}!")
            
            pickups_to_remove.append(pickup_id)

    for pickup_id in pickups_to_remove:
        del game_state.active_pickups[pickup_id]

    return notifications
