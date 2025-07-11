import curses
import sys
import traceback
import logging
import math
from ..rendering.draw_utils import draw_weapon_stats_modal, add_stat_line
from ..common.utils import get_directional_sprite, draw_box
from ..data.factions import FACTION_DATA
from ..rendering.rendering_queue import rendering_queue

def draw_inventory_menu(stdscr, car_data, car_stats, location_desc, frame_count, menu_selection, color_map, menu_preview_angle):
    """Adds the status menu modal to the rendering queue."""
    h, w = stdscr.getmaxyx()
    if h < 10 or w < 60:
        rendering_queue.add(100, stdscr.addstr, 0, 0, "Terminal too small for menu!")
        return

    menu_h = h - 4
    menu_w = w - 6
    menu_y = 2
    menu_x = 3
    
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    particle_color_pair = color_map.get("PARTICLE", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)

    # Draw the background
    for y in range(menu_y, menu_y + menu_h):
        for x in range(menu_x, menu_x + menu_w):
            rendering_queue.add(49, stdscr.addch, y, x, ' ', color_map.get("MENU_BACKGROUND", 0))

    # Draw the main box
    draw_box(stdscr, menu_y, menu_x, menu_h, menu_w, f"{car_data['name']} Status", z_index=50)

    stats_col_width = 25
    inventory_col_width = 20
    factions_col_width = 20
    stats_h = menu_h - 4
    stats_y = menu_y + 2

    factions_x = menu_x + menu_w - factions_col_width - 2
    inventory_x = factions_x - inventory_col_width - 2
    stats_x = inventory_x - stats_col_width - 2

    # --- Draw Stats ---
    stats_inner_y = stats_y + 1
    stats_inner_x = stats_x + 1
    current_stat_y = stats_inner_y
    
    add_stat_line(stdscr, current_stat_y, stats_inner_x, "Location", location_desc, text_color_pair, z_index=51)
    current_stat_y += 2
    add_stat_line(stdscr, current_stat_y, stats_inner_x, "Cash", f"${car_stats['cash']}", text_color_pair, z_index=51)
    current_stat_y += 1
    add_stat_line(stdscr, current_stat_y, stats_inner_x, "Durability", f"{car_stats['durability']}/{car_stats['max_durability']}", text_color_pair, z_index=51)
    current_stat_y += 1
    add_stat_line(stdscr, current_stat_y, stats_inner_x, "Gas", f"{car_stats['current_gas']:.0f}/{car_stats['gas_capacity']}", text_color_pair, z_index=51)
    current_stat_y += 1
    add_stat_line(stdscr, current_stat_y, stats_inner_x, "Level", car_stats['player_level'], text_color_pair, z_index=51)
    current_stat_y += 1
    xp_p = (car_stats['current_xp'] / car_stats['xp_to_next_level']) * 100 if car_stats['xp_to_next_level'] > 0 else 100
    xp_bl = 10
    xp_f = int(xp_bl * xp_p / 100)
    xp_bar_str = f"[{'█'*xp_f}{'░'*(xp_bl-xp_f)}]"
    add_stat_line(stdscr, current_stat_y, stats_inner_x, "XP", f"{xp_bar_str} {car_stats['current_xp']}/{car_stats['xp_to_next_level']}", text_color_pair, z_index=51)
    current_stat_y += 2
    rendering_queue.add(51, stdscr.addstr, current_stat_y, stats_inner_x, "Ammo:", text_color_pair)
    current_stat_y += 1
    for ammo_type, count in car_stats['ammo_counts'].items():
        rendering_queue.add(51, stdscr.addstr, current_stat_y, stats_inner_x + 2, f"- {ammo_type}: {count}", text_color_pair)
        current_stat_y += 1
    current_stat_y += 1
    rendering_queue.add(51, stdscr.addstr, current_stat_y, stats_inner_x, "Quests:", text_color_pair)
    current_stat_y += 1
    if not car_stats['quests']:
        rendering_queue.add(51, stdscr.addstr, current_stat_y, stats_inner_x + 2, "- (None)", text_color_pair)
    else:
        for quest in car_stats['quests']:
            rendering_queue.add(51, stdscr.addstr, current_stat_y, stats_inner_x + 2, f"- {quest}", text_color_pair)
            current_stat_y += 1

    # --- Draw Inventory ---
    inv_inner_y = stats_y + 1
    inv_inner_x = inventory_x + 1
    current_inv_y = inv_inner_y
    inv_header = "Inventory"
    rendering_queue.add(51, stdscr.addstr, current_inv_y, inv_inner_x + (inventory_col_width - 2 - len(inv_header)) // 2, inv_header, curses.A_UNDERLINE)
    current_inv_y += 2
    inventory_items = car_stats.get('inventory', [])
    if not inventory_items:
        rendering_queue.add(51, stdscr.addstr, current_inv_y, inv_inner_x, "(Empty)", curses.A_DIM)
    else:
        for idx, item in enumerate(inventory_items):
            is_selected = (menu_selection[0] == 1 and menu_selection[1] == idx)
            item_name = item.name
            item_str = f"- {item_name}"[:inventory_col_width-2]
            line_attr = highlight_color_pair | curses.A_BOLD if is_selected else text_color_pair
            rendering_queue.add(51, stdscr.addstr, current_inv_y, inv_inner_x, item_str.ljust(inventory_col_width - 2), line_attr)
            if is_selected:
                draw_weapon_stats_modal(stdscr, current_inv_y, inventory_x + inventory_col_width + 2, 10, 40, item, text_color_pair, z_index=60)
            current_inv_y += 1

    # --- Draw Factions ---
    draw_box(stdscr, menu_y, factions_x - 2, menu_h, factions_col_width + 2, "Factions", z_index=50)
    fac_inner_y = stats_y + 1
    fac_inner_x = factions_x + 1
    current_fac_y = fac_inner_y
    faction_reputations = car_stats.get('faction_reputation', {})
    if not faction_reputations:
        rendering_queue.add(51, stdscr.addstr, current_fac_y, fac_inner_x, "(None Known)", curses.A_DIM)
    else:
        for faction_id, rep in faction_reputations.items():
            faction_name = FACTION_DATA[faction_id]["name"]
            rep_str = f"- {faction_name}: {rep}"[:factions_col_width-2]
            rendering_queue.add(51, stdscr.addstr, current_fac_y, fac_inner_x, rep_str, text_color_pair)
            current_fac_y += 1

    # --- Draw Car Art and Mounts ---
    large_art = get_directional_sprite(car_data["menu_art"], menu_preview_angle)
    art_h = len(large_art)
    art_w = max(len(line) for line in large_art) if art_h > 0 else 0
    available_art_width = stats_x - menu_x - 3
    art_x = menu_x + max(2, (available_art_width - art_w) // 2)
    art_y = menu_y + 4
    
    from ..rendering.draw_utils import draw_sprite
    draw_sprite(stdscr, art_y, art_x, large_art, car_data.get("color_pair", text_color_pair), transparent_bg=True, z_index=50)

    mount_y = art_y + art_h + 2
    header = f"{'#':<3}{'Location':<15}{'Size':<6}{'Weapon':<12}{'Slots':<6}"
    rendering_queue.add(51, stdscr.addstr, mount_y, art_x, header, curses.A_UNDERLINE)
    mount_y += 1

    mount_index = 0
    flash_on = (frame_count // 2) % 2 == 0
    weapon_items = list(car_data['attachment_points'].items())

    for point_name, point_info in weapon_items:
        is_selected = (menu_selection[0] == 0 and menu_selection[1] == mount_index)
        weapon = car_stats['mounted_weapons'].get(point_name)
        point_size = point_info.get('size', '?')
        wep_name = "Empty"
        if weapon:
            wep_name = weapon.name
        wep_slots = weapon.slots if weapon else '?'
        mount_line = f"{mount_index+1:<3}{point_name:<15}{point_size:<6}{wep_name:<12}{wep_slots:<6}"
        line_attr = highlight_color_pair | curses.A_BOLD if is_selected else text_color_pair
        rendering_queue.add(51, stdscr.addstr, mount_y, art_x, mount_line.ljust(available_art_width - art_x), line_attr)
        if is_selected and weapon:
            draw_weapon_stats_modal(stdscr, mount_y, art_x + len(mount_line) + 2, 10, 40, weapon, text_color_pair, z_index=60)
        if is_selected:
            rel_x = point_info.get("offset_x", 0)
            rel_y = point_info.get("offset_y", 0)
            indicator_x = art_x + art_w // 2 + int(rel_x)
            indicator_y = art_y + art_h // 2 + int(rel_y)
            if rel_x > art_w * 0.3: indicator_x += 1
            elif rel_x < -art_w * 0.3: indicator_x -= 1
            if rel_y > art_h * 0.3: indicator_y += 1
            elif rel_y < -art_h * 0.3: indicator_y -= 1
            indicator_char = "●" if flash_on else str(mount_index+1)
            indicator_attr = curses.A_BOLD | color_map.get("INDICATOR_YELLOW", 0)
            rendering_queue.add(52, stdscr.addch, indicator_y, indicator_x, indicator_char, indicator_attr)
        mount_y += 1
        mount_index += 1
