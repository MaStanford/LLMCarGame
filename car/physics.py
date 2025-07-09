import math
import random
from .data.game_constants import CITY_SPACING, TOTAL_SPAWN_RATE, MAX_ENEMIES
from .data.obstacles import OBSTACLE_DATA
from .data.pickups import PICKUP_DATA, PICKUP_CASH
from .data.weapons import WEAPONS_DATA
from .data.enemies import ENEMIES_DATA
from .common.utils import get_obstacle_dimensions
from .logic.quests import KillCountObjective, SurvivalObjective
from .ui.entity_modal import play_explosion_in_modal
from .ui.notifications import add_notification

def update_physics_and_collisions(game_state, world, audio_manager, stdscr, color_pair_map):
    """Handles all physics updates and collision detection."""
    
    h, w = stdscr.getmaxyx()
    # --- Update Logic (Physics, Collisions, etc.) ---
    for wep_key in game_state.weapon_cooldowns: 
        game_state.weapon_cooldowns[wep_key] = max(0, game_state.weapon_cooldowns[wep_key] - 1)

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
        current_braking_force = game_state.braking_deceleration_factor
    
    drag_force = (game_state.drag_coefficient * (game_state.car_speed**2)) + 0.005
    speed_change = current_acceleration_force - drag_force - current_braking_force
    game_state.car_speed += speed_change

    car_center_world_x = game_state.car_world_x + game_state.car_width / 2
    car_center_world_y = game_state.car_world_y + game_state.car_height / 2
    current_terrain = world.get_terrain_at(car_center_world_x, car_center_world_y)
    terrain_speed_mod = current_terrain.get("speed_modifier", 1.0)
    effective_max_speed = game_state.max_speed * terrain_speed_mod
    game_state.car_speed = max(0, min(game_state.car_speed, effective_max_speed if effective_max_speed > 0 else 0))

    game_state.car_velocity_x = game_state.car_speed * math.cos(game_state.car_angle)
    game_state.car_velocity_y = game_state.car_speed * math.sin(game_state.car_angle)
    next_world_x = game_state.car_world_x + game_state.car_velocity_x
    next_world_y = game_state.car_world_y + game_state.car_velocity_y
    next_center_x = next_world_x + game_state.car_width / 2
    next_center_y = next_world_y + game_state.car_height / 2
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
        for point_name, wep_key in game_state.mounted_weapons.items():
            if game_state.weapon_cooldowns[wep_key] <= 0:
                wep_data = WEAPONS_DATA[wep_key]
                ammo_type = wep_data["ammo_type"]
                if game_state.ammo_counts.get(ammo_type, 0) > 0:
                    point_data = game_state.attachment_points.get(point_name)
                    if not point_data: continue
                    game_state.ammo_counts[ammo_type] -= 1
                    game_state.weapon_cooldowns[wep_key] = wep_data["fire_rate"]
                    offset_x = point_data["offset_x"]
                    offset_y = point_data["offset_y"]
                    rotated_offset_x = offset_x * math.cos(game_state.car_angle) - offset_y * math.sin(game_state.car_angle)
                    rotated_offset_y = offset_x * math.sin(game_state.car_angle) + offset_y * math.cos(game_state.car_angle)
                    forward_proj_offset = game_state.car_width * 0.5 + 1.0
                    p_x = car_center_world_x + rotated_offset_x + forward_proj_offset * math.cos(game_state.car_angle)
                    p_y = car_center_world_y + rotated_offset_y + forward_proj_offset * math.sin(game_state.car_angle)
                    projectile_power = wep_data["power"] * game_state.level_damage_modifier
                    if wep_key == "flamethrower":
                        end_x = p_x + wep_data["range"] * math.cos(game_state.car_angle)
                        end_y = p_y + wep_data["range"] * math.sin(game_state.car_angle)
                        game_state.active_flames.append([p_x, p_y, end_x, end_y, projectile_power])
                        audio_manager.play_sfx("flamethrower")
                    else:
                        game_state.active_particles.append([p_x, p_y, game_state.car_angle, wep_data["speed"], projectile_power, wep_data["range"], wep_data["particle"]])
                        audio_manager.play_sfx(wep_key)

    particles_to_remove = []
    obstacles_hit_by_projectiles = {}
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
        for obs_id, obs_state in game_state.active_obstacles.items():
            ox, oy, _, oh, ow, _, _, _, odur = obs_state
            if (ox <= p_x < ox + ow and oy <= p_y < oy + oh):
                obstacles_hit_by_projectiles[obs_id] = obstacles_hit_by_projectiles.get(obs_id, 0) + p_power
                audio_manager.play_sfx("enemy_hit")
                particles_to_remove.append(i)
                collided = True
                break
        if collided: continue
        for boss_id, boss_state in game_state.active_bosses.items():
            bx, by, _, bh, bw, _, _, _, bhp = boss_state
            if (bx <= p_x < bx + bw and by <= p_y < by + bh):
                bosses_hit_by_projectiles[boss_id] = bosses_hit_by_projectiles.get(boss_id, 0) + p_power
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

    for fx1, fy1, fx2, fy2, f_power in game_state.active_flames:
        flame_len_sq = (fx2 - fx1)**2 + (fy2 - fy1)**2
        if flame_len_sq < 1: continue
        for obs_id, obs_state in game_state.active_obstacles.items():
            ox, oy, _, oh, ow, _, _, _, odur = obs_state
            ocx = ox + ow / 2
            ocy = oy + oh / 2
            flame_min_x = min(fx1, fx2)
            flame_max_x = max(fx1, fx2)
            flame_min_y = min(fy1, fy2)
            flame_max_y = max(fy1, fy2)
            if (ox < flame_max_x and ox + ow > flame_min_x and oy < flame_max_y and oy + oh > flame_min_y):
                dist_sq = (ocx - fx1)**2 + (ocy - fy1)**2
                if dist_sq <= flame_len_sq * 1.1:
                    fdx, fdy = fx2 - fx1, fy2 - fy1
                    odx, ody = ocx - fx1, ocy - fy1
                    dot = fdx * odx + fdy * ody
                    if dot >= 0:
                        obstacles_hit_by_projectiles[obs_id] = obstacles_hit_by_projectiles.get(obs_id, 0) + f_power
    
    for boss_id, damage in bosses_hit_by_projectiles.items():
        if boss_id in game_state.active_bosses:
            game_state.active_bosses[boss_id].hp -= damage
            if game_state.active_bosses[boss_id].hp <= 0:
                boss = game_state.active_bosses[boss_id]
                play_explosion_in_modal(stdscr, boss.art, color_pair_map)
                del game_state.active_bosses[boss_id]

    obstacle_ids_to_remove = []
    pickups_to_spawn = []
    xp_gained_this_frame = 0
    for obs_id, damage in obstacles_hit_by_projectiles.items():
        if obs_id in game_state.active_obstacles:
            game_state.active_obstacles[obs_id][8] -= damage
            if game_state.active_obstacles[obs_id][8] <= 0:
                obs_state = game_state.active_obstacles[obs_id]
                obs_data = OBSTACLE_DATA[obs_state[2]]
                play_explosion_in_modal(stdscr, obs_data["art"], color_pair_map)
                audio_manager.play_sfx("explosion")
                obstacle_ids_to_remove.append(obs_id)
                
                xp_from_obstacle = obs_data.get("xp_value", 0) * game_state.difficulty_mods.get("xp_mult", 1.0)
                xp_gained_this_frame += int(xp_from_obstacle)

                if game_state.current_quest:
                    for objective in game_state.current_quest.objectives:
                        if isinstance(objective, KillCountObjective):
                            objective.kill_count += 1

                if obs_data.get("cash_value", 0) != 0:
                    pk_x = obs_state[0] + obs_state[4] / 2 + random.uniform(-0.5, 0.5)
                    pk_y = obs_state[1] + obs_state[3] / 2 + random.uniform(-0.5, 0.5)
                    pickups_to_spawn.append([pk_x, pk_y, PICKUP_CASH])
                drop = obs_data.get("drop_item")
                if drop and random.random() < obs_data.get("drop_rate", 0):
                    pk_x = obs_state[0] + obs_state[4] / 2 + random.uniform(-0.5, 0.5)
                    pk_y = obs_state[1] + obs_state[3] / 2 + random.uniform(-0.5, 0.5)
                    pickups_to_spawn.append([pk_x, pk_y, drop])
                alt_drops = obs_data.get("alt_drop_items")
                if alt_drops and random.random() < obs_data.get("alt_drop_rate", 0):
                    alt_drop_type = random.choice(alt_drops)
                    pk_x = obs_state[0] + obs_state[4] / 2 + random.uniform(-0.5, 0.5)
                    pk_y = obs_state[1] + obs_state[3] / 2 + random.uniform(-0.5, 0.5)
                    pickups_to_spawn.append([pk_x, pk_y, alt_drop_type])
    
    if xp_gained_this_frame > 0:
        game_state.gain_xp(xp_gained_this_frame)

    for obs_id in obstacle_ids_to_remove:
        if obs_id in game_state.active_obstacles:
            del game_state.active_obstacles[obs_id]
    unique_indices = sorted(list(set(particles_to_remove)), reverse=True)
    for i in unique_indices:
        if i < len(game_state.active_particles):
            del game_state.active_particles[i]
    for px, py, ptype in pickups_to_spawn:
        if ptype in PICKUP_DATA:
            pdata = PICKUP_DATA[ptype]
            game_state.active_pickups[game_state.next_pickup_id] = [px, py, ptype, pdata["art"], pdata["color_pair_name"]]
            game_state.next_pickup_id += 1

    game_state.obstacle_spawn_timer -= 1
    ids_to_remove = []
    for obs_id, obs_state in list(game_state.active_obstacles.items()):
        ox, oy, didx, oh, ow, ovx, ovy, oart, odur = obs_state
        odata = OBSTACLE_DATA[didx]
        nox = ox + ovx
        noy = oy + ovy
        nterrain = world.get_terrain_at(nox + ow / 2, noy + oh / 2)
        if nterrain.get("passable", True):
            ox, oy = nox, noy
        else:
            ovx *= -0.5
            ovy *= -0.5
        if odata["type"] == "moving":
            dx = car_center_world_x - (ox + ow / 2)
            dy = car_center_world_y - (oy + oh / 2)
            dsq = dx * dx + dy * dy
            aggro_sq = (game_state.spawn_radius * 0.8)**2
            min_dsq = (game_state.car_width + ow)**2
            if min_dsq < dsq < aggro_sq:
                dist = math.sqrt(dsq)
                ovx = (dx / dist) * odata["speed"]
                ovy = (dy / dist) * odata["speed"]
            else:
                if random.random() < 0.05:
                    wangle = random.uniform(0, 2 * math.pi)
                    wspeed = odata["speed"] * 0.5
                    ovx = math.cos(wangle) * wspeed
                    ovy = math.sin(wangle) * wspeed
                elif random.random() < 0.1:
                    ovx, ovy = 0, 0
        game_state.active_obstacles[obs_id] = [ox, oy, didx, oh, ow, ovx, ovy, oart, odur]
        dist_car_sq = (ox - game_state.car_world_x)**2 + (oy - game_state.car_world_y)**2
        if dist_car_sq > game_state.despawn_radius**2:
            ids_to_remove.append(obs_id)
    for obs_id in ids_to_remove:
        if obs_id in game_state.active_obstacles:
            del game_state.active_obstacles[obs_id]

    # --- Enemy AI and Movement ---
    enemy_ids_to_remove = []
    for enemy_id, enemy_state in list(game_state.active_enemies.items()):
        ex, ey, didx, eh, ew, evx, evy, eart, edur = enemy_state
        edata = ENEMIES_DATA[didx]
        
        # Move enemy
        nex = ex + evx
        ney = ey + evy
        nterrain = world.get_terrain_at(nex + ew / 2, ney + eh / 2)
        if nterrain.get("passable", True):
            ex, ey = nex, ney
        else:
            evx *= -0.5
            evy *= -0.5

        # AI logic
        dx = car_center_world_x - (ex + ew / 2)
        dy = car_center_world_y - (ey + eh / 2)
        dsq = dx * dx + dy * dy
        aggro_sq = (game_state.spawn_radius * 0.9)**2
        min_dsq = (game_state.car_width + ew)**2

        if min_dsq < dsq < aggro_sq:
            dist = math.sqrt(dsq)
            evx = (dx / dist) * edata["speed"]
            evy = (dy / dist) * edata["speed"]
        else:
            if random.random() < 0.05:
                wangle = random.uniform(0, 2 * math.pi)
                wspeed = edata["speed"] * 0.5
                evx = math.cos(wangle) * wspeed
                evy = math.sin(wangle) * wspeed
            elif random.random() < 0.1:
                evx, evy = 0, 0
        
        game_state.active_enemies[enemy_id] = [ex, ey, didx, eh, ew, evx, evy, eart, edur]

        # Despawn logic
        dist_car_sq = (ex - game_state.car_world_x)**2 + (ey - game_state.car_world_y)**2
        if dist_car_sq > game_state.despawn_radius**2:
            enemy_ids_to_remove.append(enemy_id)

    for enemy_id in enemy_ids_to_remove:
        if enemy_id in game_state.active_enemies:
            del game_state.active_enemies[enemy_id]

    max_obs = 20
    if game_state.obstacle_spawn_timer <= 0 and len(game_state.active_obstacles) < max_obs:
        rval = random.random() * TOTAL_SPAWN_RATE
        cum_rate = 0
        chosen_idx = -1
        for idx, odata_s in enumerate(OBSTACLE_DATA):
            cum_rate += odata_s["spawn_rate"]
            if rval <= cum_rate:
                chosen_idx = idx
                break
        if chosen_idx != -1:
            odata_s = OBSTACLE_DATA[chosen_idx]
            oh_s, ow_s = get_obstacle_dimensions(odata_s["art"])
            attempts = 0
            while attempts < 10:
                sangle = random.uniform(0, 2 * math.pi)
                sdist = random.uniform(game_state.spawn_radius * 0.8, game_state.spawn_radius)
                sx = game_state.car_world_x + sdist * math.cos(sangle)
                sy = game_state.car_world_y + sdist * math.sin(sangle)
                sterrain = world.get_terrain_at(sx + ow_s / 2, sy + oh_s / 2)
                if sterrain.get("passable", True):
                    ovx_s, ovy_s = 0, 0
                    odur_s = int(odata_s["durability"] * game_state.difficulty_mods["enemy_hp_mult"])
                    game_state.active_obstacles[game_state.next_obstacle_id] = [sx, sy, chosen_idx, oh_s, ow_s, ovx_s, ovy_s, odata_s["art"], odur_s]
                    game_state.next_obstacle_id += 1
                    game_state.obstacle_spawn_timer = random.randint(15, 40)
                    break
                attempts += 1
            if attempts == 10:
                game_state.obstacle_spawn_timer = 15

    game_state.enemy_spawn_timer -= 1
    max_enemies = MAX_ENEMIES
    if game_state.current_quest:
        for objective in game_state.current_quest.objectives:
            if isinstance(objective, SurvivalObjective) and objective.timer > 0:
                max_enemies = int(max_enemies * 1.5)
                break

    if game_state.enemy_spawn_timer <= 0 and len(game_state.active_enemies) < max_enemies:
        rval = random.random() * TOTAL_SPAWN_RATE
        cum_rate = 0
        chosen_idx = -1
        for idx, edata_s in enumerate(ENEMIES_DATA):
            cum_rate += edata_s["spawn_rate"]
            if rval <= cum_rate:
                chosen_idx = idx
                break
        if chosen_idx != -1:
            edata_s = ENEMIES_DATA[chosen_idx]
            eh_s, ew_s = get_obstacle_dimensions(edata_s["art"])
            attempts = 0
            while attempts < 10:
                sangle = random.uniform(0, 2 * math.pi)
                sdist = random.uniform(game_state.spawn_radius * 0.8, game_state.spawn_radius)
                sx = game_state.car_world_x + sdist * math.cos(sangle)
                sy = game_state.car_world_y + sdist * math.sin(sangle)
                sterrain = world.get_terrain_at(sx + ew_s / 2, sy + eh_s / 2)
                if sterrain.get("passable", True):
                    evx_s, evy_s = 0, 0
                    edur_s = int(edata_s["durability"] * game_state.difficulty_mods["enemy_hp_mult"])
                    game_state.active_enemies[game_state.next_enemy_id] = [sx, sy, chosen_idx, eh_s, ew_s, evx_s, evy_s, edata_s["art"], edur_s]
                    game_state.next_enemy_id += 1
                    game_state.enemy_spawn_timer = random.randint(15, 40)
                    break
                attempts += 1
            if attempts == 10:
                game_state.enemy_spawn_timer = 15

    collided_obs_ids = []
    pickups_from_collision = []
    car_hit_w = max(1, game_state.car_width - 2)
    car_hit_h = max(1, game_state.car_height - 2)
    car_r1 = game_state.car_world_x
    car_r2 = car_r1 + car_hit_w
    car_ry1 = game_state.car_world_y
    car_ry2 = car_ry1 + car_hit_h
    for obs_id, obs_state in list(game_state.active_obstacles.items()):
        ox, oy, didx, oh, ow, ovx, ovy, oart, odur = obs_state
        or1 = ox
        or2 = or1 + ow
        ory1 = oy
        ory2 = ory1 + oh
        if (car_r1 < or2 and car_r2 > or1 and car_ry1 < ory2 and car_ry2 > ory1):
            audio_manager.play_sfx("crash")
            odata_c = OBSTACLE_DATA[didx]
            dmg_car = int(odata_c["damage"] * game_state.difficulty_mods["enemy_dmg_mult"])
            speed_f = min(1.0, game_state.car_speed / 5.0 if game_state.car_speed > 0 else 0.0)
            act_dmg_car = max(1, int(dmg_car * speed_f))
            game_state.current_durability -= act_dmg_car
            coll_force = game_state.car_speed * game_state.selected_car_data["weight"]
            dmg_obs = max(1, int(coll_force / 5))
            game_state.active_obstacles[obs_id][8] -= dmg_obs
            push = 0.5
            dx_c = (ox + ow / 2) - car_center_world_x
            dy_c = (oy + oh / 2) - car_center_world_y
            dist_c = math.sqrt(dx_c * dx_c + dy_c * dy_c)
            if dist_c > 0.1:
                push_vx = (dx_c / dist_c) * push
                push_vy = (dy_c / dist_c) * push
                game_state.active_obstacles[obs_id][5] += push_vx
                game_state.active_obstacles[obs_id][6] += push_vy
            game_state.car_speed *= 0.7
            if game_state.active_obstacles[obs_id][8] <= 0:
                collided_obs_ids.append(obs_id)
                xp_from_obstacle_coll = odata_c.get("xp_value", 0) * game_state.difficulty_mods.get("xp_mult", 1.0)
                game_state.gain_xp(int(xp_from_obstacle_coll))
                if game_state.current_quest:
                    for objective in game_state.current_quest.objectives:
                        if isinstance(objective, KillCountObjective):
                            objective.kill_count += 1
                if odata_c.get("cash_value", 0) != 0:
                    pk_x = ox + ow / 2 + random.uniform(-0.5, 0.5)
                    pk_y = oy + oh / 2 + random.uniform(-0.5, 0.5)
                    pickups_from_collision.append([pk_x, pk_y, PICKUP_CASH])
                drop = odata_c.get("drop_item")
                if drop and random.random() < odata_c.get("drop_rate", 0):
                    pk_x = ox + ow / 2 + random.uniform(-0.5, 0.5)
                    pk_y = oy + oh / 2 + random.uniform(-0.5, 0.5)
                    pickups_from_collision.append([pk_x, pk_y, drop])
                alt_drops = odata_c.get("alt_drop_items")
                if alt_drops and random.random() < odata_c.get("alt_drop_rate", 0):
                    alt_drop_type = random.choice(alt_drops)
                    pk_x = ox + ow / 2 + random.uniform(-0.5, 0.5)
                    pk_y = oy + oh / 2 + random.uniform(-0.5, 0.5)
                    pickups_from_collision.append([pk_x, pk_y, alt_drop_type])

    for obs_id in collided_obs_ids:
        if obs_id in game_state.active_obstacles:
            del game_state.active_obstacles[obs_id]
    for px, py, ptype in pickups_from_collision:
        if ptype in PICKUP_DATA:
            pdata = PICKUP_DATA[ptype]
            game_state.active_pickups[game_state.next_pickup_id] = [px, py, ptype, pdata["art"], pdata["color_pair_name"]]
            game_state.next_pickup_id += 1

    pickups_to_remove = []
    for pid, pstate in list(game_state.active_pickups.items()):
        px, py, ptype, part, pcname = pstate
        ph = len(part)
        pw = len(part[0]) if ph > 0 else 0
        pr1 = px
        pr2 = pr1 + pw
        pry1 = py
        pry2 = pry1 + ph
        if (car_r1 < pr2 and car_r2 > pr1 and car_ry1 < pry2 and car_ry2 > pry1):
            pinfo = PICKUP_DATA[ptype]
            val = pinfo.get("value", 0)
            if ptype == "PICKUP_GAS":
                game_state.current_gas = min(game_state.gas_capacity, game_state.current_gas + val)
            elif ptype == "PICKUP_REPAIR":
                game_state.current_durability = min(game_state.max_durability, game_state.current_durability + val)
            elif ptype == "PICKUP_CASH":
                game_state.player_cash += val
            elif ptype.startswith("AMMO_"):
                akey = pinfo.get("ammo_type")
                if akey and akey in game_state.ammo_counts:
                    game_state.ammo_counts[akey] += val
            elif ptype.startswith("GUN_"):
                gun_key = pinfo.get("gun_key")
                if gun_key:
                    gun_name = WEAPONS_DATA[gun_key]["name"]
                    if not any(item.get("name") == gun_name for item in game_state.player_inventory):
                        game_state.player_inventory.append({"type": "gun", "name": gun_name})
                        add_notification(f"Picked up {gun_name}", color="MENU_HIGHLIGHT")
            pickups_to_remove.append(pid)
    for pid in pickups_to_remove:
        if pid in game_state.active_pickups:
            del game_state.active_pickups[pid]
