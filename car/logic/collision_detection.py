import random
import math
from .loot_generation import handle_enemy_loot_drop
from ..world.generation import get_buildings_in_city

# Collision physics constants
STOP_THRESHOLD = 2.0  # Speed below which collisions stop the car completely
DEFLECTION_FRAMES = 15  # Number of frames to apply deflection (~0.5s at 30fps)
DEFLECTION_STRENGTH = 3.0  # Base deflection velocity
COLLISION_IFRAMES = 15  # Invulnerability frames after a collision
SPEED_REDUCTION_FACTOR = 0.5  # How much speed is reduced on collision
PUSH_OUT_DISTANCE = 2.0  # Distance to push player away from collision


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


def _apply_deflection(game_state, other_x, other_y, other_w, other_h, damage):
    """
    Applies deflection physics when the player collides with an entity.
    Calculates ricochet direction and sets deflection state.
    """
    player = game_state.player_car

    # Calculate collision normal (direction from other entity to player)
    player_cx = player.x + player.width / 2
    player_cy = player.y + player.height / 2
    other_cx = other_x + other_w / 2
    other_cy = other_y + other_h / 2

    nx = player_cx - other_cx
    ny = player_cy - other_cy
    dist = math.sqrt(nx * nx + ny * ny)
    if dist > 0:
        nx /= dist
        ny /= dist
    else:
        # Fallback: push in the direction the car is facing
        adjusted_angle = game_state.car_angle - (math.pi / 2)
        nx = -math.cos(adjusted_angle)
        ny = -math.sin(adjusted_angle)

    # Apply speed-scaled damage
    speed_factor = max(0.3, game_state.car_speed / (game_state.max_speed if game_state.max_speed > 0 else 1))
    actual_damage = max(1, int(damage * speed_factor))
    if not game_state.god_mode:
        game_state.current_durability -= actual_damage

    if game_state.car_speed < STOP_THRESHOLD:
        # At low speeds, just stop
        game_state.car_speed = 0
        game_state.car_velocity_x = 0
        game_state.car_velocity_y = 0
    else:
        # Reduce speed and apply deflection
        game_state.car_speed *= SPEED_REDUCTION_FACTOR

        # Ricochet: reflect velocity across collision normal
        game_state.deflection_vx = nx * DEFLECTION_STRENGTH * speed_factor
        game_state.deflection_vy = ny * DEFLECTION_STRENGTH * speed_factor
        game_state.deflection_frames = DEFLECTION_FRAMES

    # Push player out of overlap
    game_state.car_world_x += nx * PUSH_OUT_DISTANCE
    game_state.car_world_y += ny * PUSH_OUT_DISTANCE
    game_state.player_car.x = game_state.car_world_x
    game_state.player_car.y = game_state.car_world_y

    # Set invulnerability frames
    game_state.collision_iframes = COLLISION_IFRAMES


def _drop_meat(game_state, x, y):
    """Drops a meat pickup at the given position."""
    pickup_id = game_state.next_pickup_id
    game_state.next_pickup_id += 1
    meat_value = random.randint(5, 15)
    game_state.active_pickups[pickup_id] = {
        "x": x, "y": y,
        "type": "cash",  # Meat sells for cash
        "value": meat_value,
        "char": "♠",
    }


def handle_collisions(game_state, world, audio_manager, app):
    """
    Handles all collision detection and resolution.
    Returns a list of notification messages.
    """
    notifications = []

    # --- Decrement i-frames ---
    if game_state.collision_iframes > 0:
        game_state.collision_iframes -= 1

    # --- Projectile Collisions ---
    projectiles_to_remove = set()

    for i, p_state in enumerate(game_state.active_particles):
        if i in projectiles_to_remove:
            continue
        p_x, p_y, _, _, p_power, _, _, _, _ = p_state

        # Check for collisions with terrain
        p_terrain = world.get_terrain_at(p_x, p_y)
        if not p_terrain.get("passable", True):
            projectiles_to_remove.add(i)
            continue

        # Check for collisions with enemies
        hit = False
        for enemy in game_state.active_enemies:
            if (enemy.x <= p_x < enemy.x + enemy.width and
                enemy.y <= p_y < enemy.y + enemy.height):
                enemy.durability -= p_power
                audio_manager.play_sfx("enemy_hit")
                projectiles_to_remove.add(i)
                if enemy.durability <= 0:
                    game_state.destroyed_this_frame.append(enemy)
                    handle_enemy_loot_drop(game_state, enemy, app)
                    notifications.append(f"Destroyed {enemy.__class__.__name__}!")
                    game_state.active_enemies.remove(enemy)
                hit = True
                break
        if hit:
            continue

        # Check for collisions with obstacles
        for obstacle in game_state.active_obstacles[:]:
            if (obstacle.x <= p_x < obstacle.x + obstacle.width and
                obstacle.y <= p_y < obstacle.y + obstacle.height):
                obstacle.durability -= p_power
                audio_manager.play_sfx("enemy_hit")
                projectiles_to_remove.add(i)
                if obstacle.durability <= 0:
                    game_state.destroyed_this_frame.append(obstacle)
                    game_state.active_obstacles.remove(obstacle)
                    game_state.gain_xp(obstacle.xp_value)
                    notifications.append(f"Destroyed {obstacle.__class__.__name__}!")
                    if obstacle.cash_value > 0:
                        game_state.player_cash += obstacle.cash_value
                hit = True
                break
        if hit:
            continue

        # Check for collisions with fauna
        for fauna in game_state.active_fauna[:]:
            if (fauna.x <= p_x < fauna.x + fauna.width and
                fauna.y <= p_y < fauna.y + fauna.height):
                fauna.durability -= p_power
                audio_manager.play_sfx("enemy_hit")
                projectiles_to_remove.add(i)
                if fauna.durability <= 0:
                    game_state.active_fauna.remove(fauna)
                    xp = getattr(fauna, 'xp_value', 1)
                    game_state.gain_xp(xp)
                    game_state.karma -= 1  # Negative karma for killing fauna
                    _drop_meat(game_state, fauna.x, fauna.y)
                    notifications.append(f"Killed {fauna.__class__.__name__}! (-1 Karma)")
                hit = True
                break

    # Remove projectiles that have collided
    if projectiles_to_remove:
        game_state.active_particles = [p for i, p in enumerate(game_state.active_particles) if i not in projectiles_to_remove]

    # --- Player-Enemy Collision (with deflection) ---
    player = game_state.player_car
    player_rect = (player.x, player.y, player.width, player.height)

    if game_state.collision_iframes <= 0:
        for enemy in game_state.active_enemies[:]:
            enemy_rect = (enemy.x, enemy.y, enemy.width, enemy.height)
            if check_collision(player_rect, enemy_rect):
                audio_manager.play_sfx("crash")

                collision_damage = getattr(enemy, "collision_damage", 5)
                _apply_deflection(game_state, enemy.x, enemy.y, enemy.width, enemy.height, collision_damage)

                # Damage the enemy too
                enemy.durability -= getattr(player, "collision_damage", 5)

                if enemy.durability <= 0:
                    game_state.destroyed_this_frame.append(enemy)
                    handle_enemy_loot_drop(game_state, enemy, app)
                    notifications.append(f"Destroyed {enemy.__class__.__name__}!")
                    game_state.active_enemies.remove(enemy)
                break  # Only handle one collision per frame

    # --- Obstacle Collisions (with deflection) ---
    if game_state.collision_iframes <= 0:
        player_rect = (game_state.player_car.x, game_state.player_car.y,
                       game_state.player_car.width, game_state.player_car.height)
        for obstacle in game_state.active_obstacles[:]:
            obstacle_rect = (obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            if check_collision(player_rect, obstacle_rect):
                audio_manager.play_sfx("crash")

                _apply_deflection(game_state, obstacle.x, obstacle.y, obstacle.width, obstacle.height, obstacle.damage)

                obstacle.durability -= 10
                if obstacle.durability <= 0:
                    game_state.destroyed_this_frame.append(obstacle)
                    game_state.active_obstacles.remove(obstacle)
                    game_state.gain_xp(obstacle.xp_value)
                    notifications.append(f"Destroyed {obstacle.__class__.__name__}!")
                    if obstacle.cash_value > 0:
                        game_state.player_cash += obstacle.cash_value
                break  # Only handle one collision per frame

    # --- Fauna Collisions (with deflection) ---
    if game_state.collision_iframes <= 0:
        player_rect = (game_state.player_car.x, game_state.player_car.y,
                       game_state.player_car.width, game_state.player_car.height)
        for fauna in game_state.active_fauna[:]:
            fauna_rect = (fauna.x, fauna.y, fauna.width, fauna.height)
            if check_collision(player_rect, fauna_rect):
                audio_manager.play_sfx("crash")

                fauna_damage = getattr(fauna, 'collision_damage', 1)
                _apply_deflection(game_state, fauna.x, fauna.y, fauna.width, fauna.height, fauna_damage)

                fauna.durability -= getattr(player, "collision_damage", 5)
                if fauna.durability <= 0:
                    game_state.active_fauna.remove(fauna)
                    xp = getattr(fauna, 'xp_value', 1)
                    game_state.gain_xp(xp)
                    game_state.karma -= 1
                    _drop_meat(game_state, fauna.x, fauna.y)
                    notifications.append(f"Ran over {fauna.__class__.__name__}! (-1 Karma)")
                break

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
            elif pickup["type"] == "narrative":
                from ..screens.narrative_dialog import NarrativeDialogScreen
                game_state.menu_open = True
                game_state.player_car.app.push_screen(NarrativeDialogScreen(pickup["data"]))

            pickups_to_remove.append(pickup_id)

    for pickup_id in pickups_to_remove:
        del game_state.active_pickups[pickup_id]

    return notifications
