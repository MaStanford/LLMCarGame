import random
import math
from .loot_generation import handle_enemy_loot_drop
from ..ui.notifications import add_notification
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

def handle_collisions(game_state, world, audio_manager, stdscr, color_pair_map):
    """
    Handles all collision detection and resolution.
    """
    # --- Projectile Collisions ---
    particles_to_remove = []
    enemies_hit_by_projectiles = {}
    bosses_hit_by_projectiles = {}
    for i, p_state in enumerate(game_state.active_particles):
        p_x, p_y, p_angle, p_speed, p_power, p_range_left, p_char = p_state
        p_dist = p_speed
        p_x += p_dist * math.cos(p_angle)
        p_y += p_dist * math.sin(p_angle)
        p_range_left -= p_dist
        if p_range_left <= 0:
            particles_to_remove.append(i)
            continue
        collided = False
        for enemy in game_state.active_enemies:
            if (enemy.x <= p_x < enemy.x + enemy.width and enemy.y <= p_y < enemy.y + enemy.height):
                enemies_hit_by_projectiles[enemy] = enemies_hit_by_projectiles.get(enemy, 0) + p_power
                audio_manager.play_sfx("enemy_hit")
                particles_to_remove.append(i)
                collided = True
                break
        if collided: continue
        for boss_id, boss in game_state.active_bosses.items():
            if (boss.x <= p_x < boss.x + boss.width and boss.y <= p_y < boss.y + boss.height):
                bosses_hit_by_projectiles[boss] = bosses_hit_by_projectiles.get(boss, 0) + p_power
                particles_to_remove.append(i)
                collided = True
                break
        if collided: continue
        p_terrain = world.get_terrain_at(p_x, p_y)
        if not p_terrain.get("passable", True):
            particles_to_remove.append(i)
            collided = True
        if not collided:
            game_state.active_particles[i] = [p_x, p_y, p_angle, p_speed, p_power, p_range_left, p_char]

    for boss, damage in bosses_hit_by_projectiles.items():
        boss.hp -= damage
        if boss.hp <= 0:
            game_state.active_explosions.append({
                "x": boss.x, "y": boss.y, "art": boss.art, 
                "start_time": game_state.frame, "duration": 30 # 30 frames
            })
            for key, b in list(game_state.active_bosses.items()):
                if b == boss:
                    del game_state.active_bosses[key]

    enemy_ids_to_remove = []
    for enemy, damage in enemies_hit_by_projectiles.items():
        enemy.durability -= damage
        if enemy.durability <= 0:
            game_state.active_explosions.append({
                "x": enemy.x, "y": enemy.y, "art": enemy.art, 
                "start_time": game_state.frame, "duration": 20 # 20 frames
            })
            enemy_ids_to_remove.append(enemy)

    for enemy in enemy_ids_to_remove:
        handle_enemy_loot_drop(game_state, enemy)
        add_notification(game_state, f"Destroyed {enemy.__class__.__name__}!", "success")
        game_state.active_enemies.remove(enemy)

    unique_indices = sorted(list(set(particles_to_remove)), reverse=True)
    for i in unique_indices:
        if i < len(game_state.active_particles):
            del game_state.active_particles[i]

    # --- Obstacle Collisions ---
    for obstacle in game_state.active_obstacles:
        if (game_state.player_car.x < obstacle.x + obstacle.width and
            game_state.player_car.x + game_state.player_car.width > obstacle.x and
            game_state.player_car.y < obstacle.y + obstacle.height and
            game_state.player_car.y + game_state.player_car.height > obstacle.y):
            
            audio_manager.play_sfx("crash")
            game_state.player_car.durability -= obstacle.damage
            obstacle.durability -= 10
            if obstacle.durability <= 0:
                game_state.active_obstacles.remove(obstacle)
                game_state.gain_xp(obstacle.xp_value)
                if random.random() < obstacle.drop_rate:
                    pass

    # --- Pickup Collisions ---
    pickups_to_remove = []
    for pickup_id, pickup in game_state.active_pickups.items():
        if (game_state.player_car.x < pickup["x"] + 1 and
            game_state.player_car.x + game_state.player_car.width > pickup["x"] and
            game_state.player_car.y < pickup["y"] + 1 and
            game_state.player_car.y + game_state.player_car.height > pickup["y"]):
            
            if pickup["type"] == "cash":
                game_state.player_cash += pickup["value"]
                add_notification(game_state, f"Picked up {pickup['value']} cash!", "success")
            elif pickup["type"] == "weapon":
                game_state.player_inventory.append(pickup["weapon"])
                add_notification(game_state, f"Picked up {pickup['weapon'].name}!", "success")
            
            pickups_to_remove.append(pickup_id)

    for pickup_id in pickups_to_remove:
        del game_state.active_pickups[pickup_id]
