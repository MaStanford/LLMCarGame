import curses
import sys
import traceback
from ..rendering.draw_utils import draw_weapon_stats_modal, add_stat_line
from ..common.utils import get_directional_sprite
from ..data.factions import FACTION_DATA

def draw_inventory_menu(stdscr, car_data, car_stats, location_desc, frame_count, menu_selection, color_map, menu_preview_angle):
    """Draws the status menu modal. Returns the menu window object or None.
        menu_selection is a tuple: (section, index) e.g., ("weapons", 0) or ("inventory", 1)
    """
    h, w = stdscr.getmaxyx()
    if h < 10 or w < 60: # Increased min width slightly for inventory
        try:
            stdscr.addstr(0, 0, "Terminal too small for menu!")
        except curses.error:
            pass
        return None

    menu_h = h - 4
    menu_w = w - 6
    menu_y = 2
    menu_x = 3
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    particle_color_pair = color_map.get("PARTICLE", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)

    border_pair = border_color_pair if 0 <= border_color_pair < curses.COLOR_PAIRS else 0
    text_pair = text_color_pair if 0 <= text_color_pair < curses.COLOR_PAIRS else 0
    particle_pair = particle_color_pair if 0 <= particle_color_pair < curses.COLOR_PAIRS else 0
    highlight_pair = highlight_color_pair if 0 <= highlight_color_pair < curses.COLOR_PAIRS else text_pair

    menu_win = None
    try:
        menu_win = curses.newwin(menu_h, menu_w, menu_y, menu_x)
        menu_win.keypad(True)

        menu_win.bkgd(' ', curses.color_pair(text_pair))
        menu_win.erase()

        menu_win.attron(curses.color_pair(border_pair))
        menu_win.box()
        menu_win.attroff(curses.color_pair(border_pair))

        menu_win.attron(curses.color_pair(text_pair))

        title = f"{car_data['name']} Status"
        if len(title) < menu_w - 2:
            try:
                menu_win.addstr(1, (menu_w - len(title)) // 2, title, curses.A_BOLD)
            except curses.error:
                pass

        stats_col_width = 25
        inventory_col_width = 20
        factions_col_width = 20
        stats_h = menu_h - 4
        stats_y = 2

        # Calculate column positions
        factions_x = menu_w - factions_col_width - 2
        inventory_x = factions_x - inventory_col_width - 2
        stats_x = inventory_x - stats_col_width - 2

        # --- Draw Stats (Middle-Left Side) ---
        if stats_h > 2 and stats_col_width > 2 and stats_x > 1:
            stats_inner_y = stats_y + 1
            stats_inner_x = stats_x + 1
            current_stat_y = stats_inner_y

            add_stat_line(menu_win, current_stat_y, stats_inner_x, f"Location: {location_desc}", stats_col_width-2)
            current_stat_y += 2
            add_stat_line(menu_win, current_stat_y, stats_inner_x, f"Cash: ${car_stats['cash']}", stats_col_width-2)
            current_stat_y += 1
            add_stat_line(menu_win, current_stat_y, stats_inner_x, f"Durability: {car_stats['durability']}/{car_stats['max_durability']}", stats_col_width-2)
            current_stat_y += 1
            add_stat_line(menu_win, current_stat_y, stats_inner_x, f"Gas: {car_stats['current_gas']:.0f}/{car_stats['gas_capacity']}", stats_col_width-2)
            current_stat_y += 1
            
            # XP and Level for Menu
            add_stat_line(menu_win, current_stat_y, stats_inner_x, f"Level: {car_stats['player_level']}", stats_col_width-2)
            current_stat_y += 1
            xp_p = (car_stats['current_xp'] / car_stats['xp_to_next_level']) * 100 if car_stats['xp_to_next_level'] > 0 else 100
            xp_bl = 10
            xp_f = int(xp_bl * xp_p / 100)
            xp_bar_str = f"[{'█'*xp_f}{'░'*(xp_bl-xp_f)}]"
            add_stat_line(menu_win, current_stat_y, stats_inner_x, f"XP: {xp_bar_str} {car_stats['current_xp']}/{car_stats['xp_to_next_level']}", stats_col_width-2)
            current_stat_y += 2

            add_stat_line(menu_win, current_stat_y, stats_inner_x, "Ammo:", stats_col_width-2)
            current_stat_y += 1
            for ammo_type, count in car_stats['ammo_counts'].items():
                add_stat_line(menu_win, current_stat_y, stats_inner_x + 2, f"- {ammo_type}: {count}", stats_col_width-4)
                current_stat_y += 1
            
            current_stat_y += 1
            add_stat_line(menu_win, current_stat_y, stats_inner_x, "Quests:", stats_col_width-2)
            current_stat_y += 1
            if not car_stats['quests']:
                menu_win.addstr(current_stat_y, stats_inner_x + 2, f"- (None)", stats_col_width-4)
            else:
                for quest in car_stats['quests']:
                    add_stat_line(menu_win, current_stat_y, stats_inner_x + 2, f"- {quest}", stats_col_width-4)
                    current_stat_y += 1

        # --- Draw Inventory (Middle Side) ---
        if stats_h > 2 and inventory_col_width > 2 and inventory_x > 1:
            inv_inner_y = stats_y + 1
            inv_inner_x = inventory_x + 1
            current_inv_y = inv_inner_y

            inv_header = "Inventory"
            if len(inv_header) < inventory_col_width - 1:
                try:
                    menu_win.addstr(current_inv_y, inv_inner_x + (inventory_col_width - 2 - len(inv_header)) // 2, inv_header, curses.A_UNDERLINE)
                except curses.error:
                    pass
            current_inv_y += 2

            inventory_items = car_stats.get('inventory', [])
            if not inventory_items:
                if current_inv_y < menu_h - 2:
                    try:
                        menu_win.addstr(current_inv_y, inv_inner_x, "(Empty)", curses.A_DIM)
                    except curses.error:
                        pass
            else:
                for idx, item in enumerate(inventory_items):
                    if current_inv_y < menu_h - 2:
                        is_selected = (menu_selection[0] == "inventory" and menu_selection[1] == idx)
                        item_name = item.name
                        item_str = f"- {item_name}"[:inventory_col_width-2]
                        line_attr = curses.color_pair(highlight_pair) | curses.A_BOLD if is_selected else curses.color_pair(text_pair)
                        try:
                            padded_line = item_str.ljust(inventory_col_width - 2)
                            menu_win.addstr(current_inv_y, inv_inner_x, padded_line, line_attr)
                            if is_selected:
                                draw_weapon_stats_modal(stdscr, item, current_inv_y, inventory_x + inventory_col_width + 2)
                        except curses.error:
                            pass
                        current_inv_y += 1

        # --- Draw Factions (Rightmost Side) ---
        if stats_h > 2 and factions_col_width > 2 and factions_x > 1:
            sep_x_fac = factions_x - 1
            if sep_x_fac > 1:
                menu_win.attron(curses.color_pair(border_pair))
                for y_pos in range(stats_y, stats_y + stats_h):
                    if y_pos < menu_h -1:
                        try:
                            menu_win.addch(y_pos, sep_x_fac, curses.ACS_VLINE)
                        except curses.error:
                            pass
                menu_win.attroff(curses.color_pair(border_pair))

            fac_inner_y = stats_y + 1
            fac_inner_x = factions_x + 1
            current_fac_y = fac_inner_y

            fac_header = "Factions"
            if len(fac_header) < factions_col_width - 1:
                try:
                    menu_win.addstr(current_fac_y, fac_inner_x + (factions_col_width - 2 - len(fac_header)) // 2, fac_header, curses.A_UNDERLINE)
                except curses.error:
                    pass
            current_fac_y += 2

            faction_reputations = car_stats.get('faction_reputation', {})
            if not faction_reputations:
                if current_fac_y < menu_h - 2:
                    try:
                        menu_win.addstr(current_fac_y, fac_inner_x, "(None Known)", curses.A_DIM)
                    except curses.error:
                        pass
            else:
                for faction_id, rep in faction_reputations.items():
                    if current_fac_y < menu_h - 2:
                        faction_name = FACTION_DATA[faction_id]["name"]
                        rep_str = f"- {faction_name}: {rep}"[:factions_col_width-2]
                        line_attr = curses.color_pair(text_pair)
                        try:
                            menu_win.addstr(current_fac_y, fac_inner_x, rep_str, line_attr)
                        except curses.error:
                            pass
                        current_fac_y += 1
        
        # ... (rest of the drawing logic remains the same)
        
        return menu_win
    except Exception:
        # In case of any other error, end curses and print the traceback
        curses.endwin()
        print("Error in draw_inventory_menu:")
        traceback.print_exc()
        sys.exit(1)
    finally:
        if menu_win:
            menu_win.refresh()
