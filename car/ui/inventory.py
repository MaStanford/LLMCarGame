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
            # ... (stat drawing logic remains the same)

        # --- Draw Inventory (Middle Side) ---
        if stats_h > 2 and inventory_col_width > 2 and inventory_x > 1:
            # ... (inventory drawing logic remains the same)

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
        # ... (exception handling remains the same)
    finally:
        if menu_win:
            menu_win.refresh()
