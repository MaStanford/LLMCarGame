import curses
import math
from .draw_utils import draw_sprite, draw_line
from ..data.game_constants import CITY_SPACING, CITY_SIZE
from ..world.generation import get_buildings_in_city, get_city_name
from ..data.cosmetics import BUILDING_OUTLINE
from ..data.weapons import WEAPONS_DATA
from ..logic.quests import KillBossObjective
from ..data.buildings import BUILDING_DATA
from .rendering_queue import rendering_queue
import logging

def render_game(stdscr, game_state, world, color_pair_map):
    """Renders the entire game screen."""
    logging.info("RENDERER: Starting game render.")
    h, w = stdscr.getmaxyx()
    stdscr.erase()

    # Render world terrain
    world_start_x = game_state.car_world_x - w / 2
    world_start_y = game_state.car_world_y - h / 2
    for sy_draw_terrain in range(h - 1):
        for sx_draw_terrain in range(w - 1):
            cwx = world_start_x + sx_draw_terrain
            cwy = world_start_y + sy_draw_terrain
            terrain = world.get_terrain_at(cwx, cwy)
            tchar = terrain["char"]
            tcnum = color_pair_map.get(terrain["color_pair_name"], 0)
            pair_num = tcnum if 0 <= tcnum < curses.COLOR_PAIRS else 0
            rendering_queue.add(0, stdscr.addch, sy_draw_terrain, sx_draw_terrain, tchar, curses.color_pair(pair_num))

    # Render buildings
    min_gx = math.floor((world_start_x - CITY_SIZE / 2) / CITY_SPACING)
    max_gx = math.ceil((world_start_x + w + CITY_SIZE / 2) / CITY_SPACING)
    min_gy = math.floor((world_start_y - CITY_SIZE / 2) / CITY_SPACING)
    max_gy = math.ceil((world_start_y + h + CITY_SIZE / 2) / CITY_SPACING)
    for gx_draw in range(min_gx, max_gx + 1):
        for gy_draw in range(min_gy, max_gy + 1):
            buildings_in_city = get_buildings_in_city(gx_draw, gy_draw)
            for b in buildings_in_city:
                b_screen_x = b["x"] - world_start_x
                b_screen_y = b["y"] - world_start_y
                if b_screen_x + b["w"] > 0 and b_screen_x < w and b_screen_y + b["h"] > 0 and b_screen_y < h:
                    b_data = BUILDING_DATA.get(b.get("type"))
                    if b_data:
                        b_art = b_data["art"]
                        b_cname = b_data["color_pair_name"]
                        b_cnum = color_pair_map.get(b_cname, 0)
                        draw_sprite(stdscr, b_screen_y, b_screen_x, b_art, b_cnum)
                    else:
                        draw_building_outline(stdscr, b_screen_x, b_screen_y, b["w"], b["h"], b.get("name", ""), color_pair_map)

    # Render entities
    for fauna in game_state.active_fauna:
        fauna.draw(stdscr, game_state, world_start_x, world_start_y, color_pair_map)

    for obstacle in game_state.active_obstacles:
        obstacle.draw(stdscr, game_state, world_start_x, world_start_y, color_pair_map)

    for enemy in game_state.active_enemies:
        enemy.draw(stdscr, game_state, world_start_x, world_start_y, color_pair_map)

    for entity in game_state.all_entities:
        entity.draw(stdscr, game_state, world_start_x, world_start_y, color_pair_map)

    for pid, pstate in game_state.active_pickups.items():
        px, py, _, part, pcname = pstate
        psx = px - world_start_x
        psy = py - world_start_y
        pcnum = color_pair_map.get(pcname, 0)
        ph_pickup = len(part)
        pw_pickup = len(part[0]) if ph_pickup > 0 else 0
        if psx + pw_pickup > 0 and psx < w and psy + ph_pickup > 0 and psy < h:
            draw_sprite(stdscr, psy, psx, part, pcnum, transparent_bg=True)

    for p_state in game_state.active_particles:
        p_x, p_y, _, _, _, _, p_char = p_state
        p_screen_x = p_x - world_start_x
        p_screen_y = p_y - world_start_y
        if 0 <= p_screen_x < w and 0 <= p_screen_y < h:
            draw_sprite(stdscr, p_screen_y, p_screen_x, [p_char], color_pair_map.get("PARTICLE", 0))

    for fx1, fy1, fx2, fy2, _ in game_state.active_flames:
        sx1 = fx1 - world_start_x
        sy1 = fy1 - world_start_y
        sx2 = fx2 - world_start_x
        sy2 = fy2 - world_start_y
        draw_line(stdscr, sy1, sx1, sy2, sx2, "~", color_pair_map.get("FLAME", 0))

    # Render player car
    # Adjust angle for sprite direction (art is designed with 0 radians as East)
    positive_angle = (game_state.car_angle + math.pi / 2) % (2 * math.pi)
    dir_idx = int((positive_angle + math.pi / 8) / (math.pi / 4)) % 8
    direction_keys = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"] # This order is correct for the new angle setup
    direction = direction_keys[dir_idx]
    
    current_art = game_state.player_car.art[direction]
    car_sx = w / 2 - game_state.player_car.width / 2
    car_sy = h / 2 - game_state.player_car.height / 2
    draw_sprite(stdscr, car_sy, car_sx, current_art, game_state.car_color_pair_num, transparent_bg=True)

    # Render mounted weapons
    # Adjust angle for world coordinates (0 is North, but math functions treat 0 as East)
    adjusted_angle = game_state.car_angle
    car_cos = math.cos(adjusted_angle)
    car_sin = math.sin(adjusted_angle)
    
    for point_name, weapon in game_state.mounted_weapons.items():
        if weapon:
            point_data = game_state.attachment_points.get(point_name)
            if point_data:
                wep_art = weapon.art[direction]
                
                # Muzzle position in car's local space
                muzzle_local_x = point_data["offset_x"]
                muzzle_local_y = point_data["offset_y"]
                
                # Rotated muzzle position
                rotated_muzzle_x = muzzle_local_x * car_cos - muzzle_local_y * car_sin
                rotated_muzzle_y = muzzle_local_x * car_sin + muzzle_local_y * car_cos
                
                # Final weapon position on screen
                wep_sx = car_sx + game_state.player_car.width / 2 + rotated_muzzle_x
                wep_sy = car_sy + game_state.player_car.height / 2 + rotated_muzzle_y
                
                draw_sprite(stdscr, wep_sy, wep_sx, wep_art, game_state.car_color_pair_num, transparent_bg=True)

    # Render UI
    render_ui(stdscr, game_state, color_pair_map)

def draw_building_outline(stdscr, bsx, bsy, bw, bh, name, color_pair_map):
    """Adds a building outline to the rendering queue."""
    rendering_queue.add(1, _draw_building_outline_internal, stdscr, bsx, bsy, bw, bh, name, color_pair_map)

def _draw_building_outline_internal(stdscr, bsx, bsy, bw, bh, name, color_pair_map):
    h, w = stdscr.getmaxyx()
    outline_pair_num = color_pair_map.get("BUILDING_OUTLINE_COLOR", 0)
    bsx, bsy = int(round(bsx)), int(round(bsy))
    try:
        stdscr.attron(curses.color_pair(outline_pair_num))
        if 0 <= bsy < h and 0 <= bsx < w:
            stdscr.addch(bsy, bsx, BUILDING_OUTLINE["topLeft"])
        if 0 <= bsy < h and 0 <= bsx + bw - 1 < w:
            stdscr.addch(bsy, bsx + bw - 1, BUILDING_OUTLINE["topRight"])
        if 0 <= bsy + bh - 1 < h and 0 <= bsx < w:
            stdscr.addch(bsy + bh - 1, bsx, BUILDING_OUTLINE["bottomLeft"])
        if 0 <= bsy + bh - 1 < h and 0 <= bsx + bw - 1 < w:
            stdscr.addch(bsy + bh - 1, bsx + bw - 1, BUILDING_OUTLINE["bottomRight"])
        for x_outline in range(bsx + 1, bsx + bw - 1):
            if 0 <= bsy < h and 0 <= x_outline < w:
                stdscr.addch(bsy, x_outline, BUILDING_OUTLINE["horizontal"])
            if 0 <= bsy + bh - 1 < h and 0 <= x_outline < w:
                stdscr.addch(bsy + bh - 1, x_outline, BUILDING_OUTLINE["horizontal"])
        for y_outline in range(bsy + 1, bsy + bh - 1):
            if 0 <= y_outline < h and 0 <= bsx < w:
                stdscr.addch(y_outline, bsx, BUILDING_OUTLINE["vertical"])
            if 0 <= y_outline < h and 0 <= bsx + bw - 1 < w:
                stdscr.addch(y_outline, bsx + bw - 1, BUILDING_OUTLINE["vertical"])
        name_y = bsy + 1
        if 0 <= name_y < h and bh > 2:
            name_x_start = bsx + 1
            max_name_w = bw - 2
            if max_name_w > 0 and len(name) <= max_name_w:
                name_draw_x = name_x_start + (max_name_w - len(name)) // 2
                if name_draw_x >= bsx + 1:
                    stdscr.addstr(name_y, name_draw_x, name)
    except curses.error:
        pass
    finally:
        try:
            stdscr.attroff(curses.color_pair(outline_pair_num))
        except curses.error:
            pass

def render_ui(stdscr, game_state, color_pair_map):
    h, w = stdscr.getmaxyx()
    if h > 7 and w > 40:
        ctrl1 = "WASD/Arrows: Steer & Accel/Brake"
        ctrl2 = "SPACE: Fire"
        ctrl3 = "ESC: Quit | TAB: Menu"
        rendering_queue.add(20, stdscr.addstr, 0, 1, ctrl1)
        rendering_queue.add(20, stdscr.addstr, 1, 1, ctrl2)
        rendering_queue.add(20, stdscr.addstr, 2, 1, ctrl3)

        grid_x = round(game_state.car_world_x / CITY_SPACING)
        grid_y = round(game_state.car_world_y / CITY_SPACING)
        loc_desc_ui = get_city_name(grid_x, grid_y)
        loc_line = f"Loc: {loc_desc_ui}"
        loc_sc = max(1, (w - len(loc_line)) // 2)
        loc_color_pair = color_pair_map.get("UI_LOCATION", 0)
        loc_pair = loc_color_pair if 0 <= loc_color_pair < curses.COLOR_PAIRS else 0
        rendering_queue.add(20, stdscr.addstr, 0, loc_sc, loc_line, curses.color_pair(loc_pair))
        
        if game_state.current_quest and any(isinstance(o, KillBossObjective) for o in game_state.current_quest.objectives):
            for quest_key, boss in game_state.active_bosses.items():
                angle_to_boss = math.atan2(boss.y - game_state.car_world_y, boss.x - game_state.car_world_x)
                angle_diff = (angle_to_boss - game_state.car_angle + math.pi) % (2 * math.pi) - math.pi
                compass = ""
                # 16-point compass logic mapping to 8 distinct, readable arrows.
                # Each of the 16 slices is 22.5 degrees (math.pi / 8).
                slice = math.pi / 8

                # The angle_diff is from -pi to pi. A positive value is to the player's right.
                if -slice/2 <= angle_diff < slice/2:        # -11.25 to 11.25 deg
                    compass = "↑"  # N
                elif slice/2 <= angle_diff < 3*slice/2:     # 11.25 to 33.75 deg
                    compass = "↗"  # NNE
                elif 3*slice/2 <= angle_diff < 5*slice/2:   # 33.75 to 56.25 deg
                    compass = "↗"  # NE
                elif 5*slice/2 <= angle_diff < 7*slice/2:   # 56.25 to 78.75 deg
                    compass = "→"  # ENE
                elif 7*slice/2 <= angle_diff < 9*slice/2:   # 78.75 to 101.25 deg
                    compass = "→"  # E
                elif 9*slice/2 <= angle_diff < 11*slice/2:  # 101.25 to 123.75 deg
                    compass = "↘"  # ESE
                elif 11*slice/2 <= angle_diff < 13*slice/2: # 123.75 to 146.25 deg
                    compass = "↘"  # SE
                elif 13*slice/2 <= angle_diff < 15*slice/2: # 146.25 to 168.75 deg
                    compass = "↓"  # SSE
                elif angle_diff >= 15*slice/2 or angle_diff < -15*slice/2: # 168.75 to 180, and -180 to -168.75 deg
                    compass = "↓"  # S
                elif -15*slice/2 <= angle_diff < -13*slice/2:# -168.75 to -146.25 deg
                    compass = "↓"  # SSW
                elif -13*slice/2 <= angle_diff < -11*slice/2:# -146.25 to -123.75 deg
                    compass = "↙"  # SW
                elif -11*slice/2 <= angle_diff < -9*slice/2: # -123.75 to -101.25 deg
                    compass = "↙"  # WSW
                elif -9*slice/2 <= angle_diff < -7*slice/2:  # -101.25 to -78.75 deg
                    compass = "←"  # W
                elif -7*slice/2 <= angle_diff < -5*slice/2:  # -78.75 to -56.25 deg
                    compass = "←"  # WNW
                elif -5*slice/2 <= angle_diff < -3*slice/2:  # -56.25 to -33.75 deg
                    compass = "↖"  # NW
                elif -3*slice/2 <= angle_diff < -slice/2:   # -33.75 to -11.25 deg
                    compass = "↖"  # NNW
                else:
                    compass = "?" # Fallback, should not be reached
                rendering_queue.add(20, stdscr.addstr, 1, w - 20, f"Boss: {compass}")

                boss_hp_p = (boss.hp / (boss.car["durability"] * boss.hp_multiplier)) * 100
                boss_hp_bl = 20
                boss_hp_f = int(boss_hp_bl * boss_hp_p / 100)
                boss_hp_bar = f"[{'█'*boss_hp_f}{'░'*(boss_hp_bl-boss_hp_f)}]"
                rendering_queue.add(20, stdscr.addstr, 0, w - 40, f"Boss HP: {boss_hp_bar}")

        cname = f"Car: {game_state.player_car.__class__.__name__.replace('_', ' ').title()}"
        dur_p = (game_state.current_durability / game_state.max_durability) * 100 if game_state.max_durability > 0 else 0
        dur_bl = 10
        dur_f = int(dur_bl * dur_p / 100)
        dur_bar = f"[{'█'*dur_f}{'░'*(dur_bl-dur_f)}]"
        stat1 = f"Dur: {dur_bar} {int(game_state.current_durability)}/{int(game_state.max_durability)}"
        gas_p = (game_state.current_gas / game_state.gas_capacity) * 100 if game_state.gas_capacity > 0 else 0
        gas_bl = 10
        gas_f = int(gas_bl * gas_p / 100)
        gas_bar = f"[{'█'*gas_f}{'░'*(gas_bl-gas_f)}]"
        stat2 = f"Gas: {gas_bar} {game_state.current_gas:.0f}/{int(game_state.gas_capacity)}"
        stat3 = f"Speed: {game_state.car_speed:.1f}"
        stat4 = f"Cash: ${game_state.player_cash}"
        
        ammo_lns = []
        for weapon in game_state.mounted_weapons.values():
            if weapon:
                weapon_data = WEAPONS_DATA[weapon.weapon_type_id]
                ammo_type = weapon_data["ammo_type"]
                ammo_count = game_state.ammo_counts.get(ammo_type, 0)
                ammo_lns.append(f"{weapon_data['name']}: {ammo_count}")
        ammo_disp = " | ".join(ammo_lns)
        
        diff_disp = f"Difficulty: {game_state.difficulty}"
        level_disp = f"Level: {game_state.player_level}"
        xp_p_ui = (game_state.current_xp / game_state.xp_to_next_level) * 100 if game_state.xp_to_next_level > 0 else 100
        xp_bl_ui = 10
        xp_f_ui = int(xp_bl_ui * xp_p_ui / 100)
        xp_bar_str_ui = f"[{'█'*xp_f_ui}{'░'*(xp_bl_ui-xp_f_ui)}]"
        xp_disp = f"XP: {xp_bar_str_ui} {game_state.current_xp}/{game_state.xp_to_next_level}"
        quest_disp = ""
        if game_state.current_quest:
            quest_disp = f"Quest: {game_state.current_quest.name}"

        all_stats = [cname, stat1, stat2, stat3, stat4, ammo_disp, diff_disp, level_disp, xp_disp, quest_disp]
        max_len = max(len(s) for s in all_stats) if all_stats else 0
        sc_stats = max(1, w - max_len - 1)
        for i, stat_line in enumerate(all_stats):
            if i < h:
                rendering_queue.add(20, stdscr.addstr, i, sc_stats, stat_line)
