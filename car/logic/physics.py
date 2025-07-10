import math
import random
from ..data.game_constants import CITY_SPACING, MAX_ENEMIES
from ..data.pickups import PICKUP_DATA, PICKUP_CASH
from ..data.weapons import WEAPONS_DATA
from ..common.utils import get_obstacle_dimensions
from .quests import KillCountObjective, SurvivalObjective
from ..ui.entity_modal import play_explosion_in_modal
from ..ui.notifications import add_notification

def update_physics_and_collisions(game_state, world, audio_manager, stdscr, color_pair_map):
    """Handles all physics updates and collision detection."""
    
    h, w = stdscr.getmaxyx()
    # --- Update Logic (Physics, Collisions, etc.) ---
    for wep_instance_id in game_state.weapon_cooldowns: 
        game_state.weapon_cooldowns[wep_instance_id] = max(0, game_state.weapon_cooldowns[wep_instance_id] - 1)

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

    game_state.active_flames.clear()
    if game_state.actions["fire"]:
        for point_name, weapon in game_state.mounted_weapons.items():
            if weapon and game_state.weapon_cooldowns[weapon.instance_id] <= 0:
                ammo_type = weapon.ammo_type
                if game_state.ammo_counts.get(ammo_type, 0) > 0:
                    point_data = game_state.attachment_points.get(point_name)
                    if not point_data: continue
                    game_state.ammo_counts[ammo_type] -= 1
                    game_state.weapon_cooldowns[weapon.instance_id] = weapon.fire_rate
                    offset_x = point_data["offset_x"]
                    offset_y = point_data["offset_y"]
                    rotated_offset_x = offset_x * math.cos(game_state.car_angle) - offset_y * math.sin(game_state.car_angle)
                    rotated_offset_y = offset_x * math.sin(game_state.car_angle) + offset_y * math.cos(game_state.car_angle)
                    forward_proj_offset = game_state.player_car.width * 0.5 + 1.0
                    p_x = car_center_world_x + rotated_offset_x + forward_proj_offset * math.cos(game_state.car_angle)
                    p_y = car_center_world_y + rotated_offset_y + forward_proj_offset * math.sin(game_state.car_angle)
                    projectile_power = weapon.damage * game_state.level_damage_modifier
                    
                    for i in range(weapon.pellet_count):
                        angle_offset = 0
                        if weapon.pellet_count > 1:
                            angle_offset = (i - (weapon.pellet_count - 1) / 2) * weapon.spread_angle / (weapon.pellet_count -1)
                        
                        p_angle = game_state.car_angle + angle_offset

                        if weapon.weapon_type_id == "wep_flamethrower":
                            end_x = p_x + weapon.range * math.cos(p_angle)
                            end_y = p_y + weapon.range * math.sin(p_angle)
                            game_state.active_flames.append([p_x, p_y, end_x, end_y, projectile_power])
                            audio_manager.play_sfx("flamethrower")
                        else:
                            game_state.active_particles.append([p_x, p_y, p_angle, weapon.speed, projectile_power, weapon.range, weapon.particle])
                            audio_manager.play_sfx(weapon.weapon_type_id)

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
            play_explosion_in_modal(stdscr, boss.art, color_pair_map)
            # This needs to be handled better
            for key, b in list(game_state.active_bosses.items()):
                if b == boss:
                    del game_state.active_bosses[key]

    enemy_ids_to_remove = []
    for enemy, damage in enemies_hit_by_projectiles.items():
        enemy.durability -= damage
        if enemy.durability <= 0:
            enemy_ids_to_remove.append(enemy)

    for enemy in enemy_ids_to_remove:
        game_state.active_enemies.remove(enemy)

    unique_indices = sorted(list(set(particles_to_remove)), reverse=True)
    for i in unique_indices:
        if i < len(game_state.active_particles):
            del game_state.active_particles[i]

    # --- Enemy AI and Movement ---
    for enemy in game_state.active_enemies:
        enemy.update(game_state, world)
        
    # Despawn logic
    game_state.active_enemies = [e for e in game_state.active_enemies if (e.x - game_state.car_world_x)**2 + (e.y - game_state.car_world_y)**2 < game_state.despawn_radius**2]
    game_state.active_fauna = [f for f in game_state.active_fauna if (f.x - game_state.car_world_x)**2 + (f.y - game_state.car_world_y)**2 < game_state.despawn_radius**2]
    game_state.active_obstacles = [o for o in game_state.active_obstacles if (o.x - game_state.car_world_x)**2 + (o.y - game_state.car_world_y)**2 < game_state.despawn_radius**2]

    # Collision with obstacles
    for obstacle in game_state.active_obstacles:
        if (game_state.player_car.x < obstacle.x + obstacle.width and
            game_state.player_car.x + game_state.player_car.width > obstacle.x and
            game_state.player_car.y < obstacle.y + obstacle.height and
            game_state.player_car.y + game_state.player_car.height > obstacle.y):
            
            audio_manager.play_sfx("crash")
            game_state.player_car.durability -= obstacle.damage
            obstacle.durability -= 10 # Arbitrary damage to obstacle
            if obstacle.durability <= 0:
                game_state.active_obstacles.remove(obstacle)
                game_state.gain_xp(obstacle.xp_value)
                if random.random() < obstacle.drop_rate:
                    # This needs to be implemented properly
                    pass
