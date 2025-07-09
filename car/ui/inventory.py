import curses

def draw_inventory_menu(stdscr, car_data, car_stats, location_desc, frame_count, menu_selection, color_map):
    """Draws the status menu modal. Returns the menu window object or None.
        menu_selection is a tuple: (section, index) e.g., ("weapons", 0) or ("inventory", 1)
    """
    h, w = stdscr.getmaxyx()
    if h < 10 or w < 60: # Increased min width slightly for inventory
        try: stdscr.addstr(0, 0, "Terminal too small for menu!")
        except curses.error: pass
        return None

    menu_h = h - 4; menu_w = w - 6; menu_y = 2; menu_x = 3
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
            try: menu_win.addstr(1, (menu_w - len(title)) // 2, title, curses.A_BOLD)
            except curses.error: pass

        stats_col_width = 25
        inventory_col_width = 20 # Width for inventory section
        stats_h = menu_h - 4
        stats_y = 2

        # Calculate column positions
        inventory_x = menu_w - inventory_col_width - 2
        stats_x = inventory_x - stats_col_width - 2 # Stats left of inventory

        # --- Draw Stats (Middle-Right Side) ---
        if stats_h > 2 and stats_col_width > 2 and stats_x > 1:
            # Draw separator left of stats
            sep_x_left = stats_x - 1
            if sep_x_left > 1:
                menu_win.attron(curses.color_pair(border_pair))
                for y_pos in range(stats_y, stats_y + stats_h):
                    if y_pos < menu_h -1:
                        try: menu_win.addch(y_pos, sep_x_left, curses.ACS_VLINE)
                        except curses.error: pass
                menu_win.attroff(curses.color_pair(border_pair))

            stats_inner_y = stats_y + 1
            stats_inner_x = stats_x + 1
            current_stat_y = stats_inner_y
            def add_stat_line(y, x, text, max_w):
                nonlocal current_stat_y
                max_y, max_x = menu_win.getmaxyx()
                if y < max_y -1 and x < max_x -1 :
                    try: menu_win.addstr(y, x, text[:max_w])
                    except curses.error: pass
                current_stat_y += 1

            add_stat_line(current_stat_y, stats_inner_x, f"Location: {location_desc}", stats_col_width-2)
            current_stat_y += 1
            add_stat_line(current_stat_y, stats_inner_x, f"Cash: ${car_stats['cash']}", stats_col_width-2)
            add_stat_line(current_stat_y, stats_inner_x, f"Durability: {car_stats['durability']}/{car_stats['max_durability']}", stats_col_width-2)
            add_stat_line(current_stat_y, stats_inner_x, f"Gas: {car_stats['current_gas']:.0f}/{car_stats['gas_capacity']}", stats_col_width-2)
            
            # XP and Level for Menu
            add_stat_line(current_stat_y, stats_inner_x, f"Level: {car_stats['player_level']}", stats_col_width-2)
            xp_p = (car_stats['current_xp'] / car_stats['xp_to_next_level']) * 100 if car_stats['xp_to_next_level'] > 0 else 100
            xp_bl = 10; xp_f = int(xp_bl * xp_p / 100);
            xp_bar_str = f"[{'█'*xp_f}{'░'*(xp_bl-xp_f)}]"
            add_stat_line(current_stat_y, stats_inner_x, f"XP: {xp_bar_str} {car_stats['current_xp']}/{car_stats['xp_to_next_level']}", stats_col_width-2)

            current_stat_y += 1
            add_stat_line(current_stat_y, stats_inner_x, "Ammo:", stats_col_width-2)
            for ammo_type, count in car_stats['ammo_counts'].items():
                add_stat_line(current_stat_y, stats_inner_x + 2, f"- {ammo_type}: {count}", stats_col_width-4)
            
            current_stat_y += 1
            add_stat_line(current_stat_y, stats_inner_x, "Quests:", stats_col_width-2)
            if not car_stats['quests']:
                add_stat_line(current_stat_y, stats_inner_x + 2, "- (None)", stats_col_width-4)
            else:
                for quest in car_stats['quests']:
                    add_stat_line(current_stat_y, stats_inner_x + 2, f"- {quest}", stats_col_width-4)


        # --- Draw Inventory (Rightmost Side) ---
        if stats_h > 2 and inventory_col_width > 2 and inventory_x > 1:
            # Draw separator left of inventory
            sep_x_inv = inventory_x - 1
            if sep_x_inv > 1:
                menu_win.attron(curses.color_pair(border_pair))
                for y_pos in range(stats_y, stats_y + stats_h):
                    if y_pos < menu_h -1:
                        try: menu_win.addch(y_pos, sep_x_inv, curses.ACS_VLINE)
                        except curses.error: pass
                menu_win.attroff(curses.color_pair(border_pair))

            inv_inner_y = stats_y + 1
            inv_inner_x = inventory_x + 1
            current_inv_y = inv_inner_y

            inv_header = "Inventory"
            if len(inv_header) < inventory_col_width - 1:
                try: menu_win.addstr(current_inv_y, inv_inner_x + (inventory_col_width - 2 - len(inv_header)) // 2, inv_header, curses.A_UNDERLINE)
                except curses.error: pass
            current_inv_y += 2

            inventory_items = car_stats.get('inventory', [])
            if not inventory_items:
                if current_inv_y < menu_h - 2:
                    try: menu_win.addstr(current_inv_y, inv_inner_x, "(Empty)", curses.A_DIM)
                    except curses.error: pass
            else:
                for idx, item in enumerate(inventory_items):
                    if current_inv_y < menu_h - 2:
                        is_selected = (menu_selection[0] == "inventory" and menu_selection[1] == idx)
                        item_name = item.get("name", "Unknown Item")
                        item_str = f"- {item_name}"[:inventory_col_width-2]
                        line_attr = curses.color_pair(highlight_pair) | curses.A_BOLD if is_selected else curses.color_pair(text_pair)
                        try:
                            padded_line = item_str.ljust(inventory_col_width - 2)
                            menu_win.addstr(current_inv_y, inv_inner_x, padded_line, line_attr)
                        except curses.error: pass
                        current_inv_y += 1


        # --- Draw Car Art and Mounts (Left Side) ---
        large_art = car_data.get("menu_art", ["No Art"]); art_h = len(large_art)
        art_w = max(len(line) for line in large_art) if art_h > 0 else 0
        available_art_width = stats_x - 3 # Width available left of stats
        art_x = max(2, (available_art_width - art_w) // 2)
        art_y = 4

        if art_x + art_w < available_art_width:
            for i, line in enumerate(large_art):
                if art_y + i < menu_h - 1:
                    try: menu_win.addstr(art_y + i, art_x, line)
                    except curses.error: pass

        mount_y = art_y + art_h + 2
        header = f"{'#':<3}{'Location':<15}{'Size':<6}{'Weapon':<12}{'Slots':<6}"
        if mount_y < menu_h - 2 and art_x + len(header) < available_art_width:
            try: menu_win.addstr(mount_y, art_x, header, curses.A_UNDERLINE); mount_y += 1
            except curses.error: pass

        # Draw Weapon List with Highlighting
        mount_index = 0 # Use 0-based index for selection logic
        flash_on = (frame_count // 15) % 2 == 0
        weapon_items = list(car_data['mounted_weapons'].items()) # Get weapons as a list

        for point_name, wep_key in weapon_items:
            is_selected = (menu_selection[0] == "weapons" and menu_selection[1] == mount_index)
            point_info = car_data['attachment_points'].get(point_name, {})
            point_size = point_info.get('size', '?'); wep_name = "Empty"
            if wep_key:
                wep_name = car_data['weapons_data'].get(wep_key, {}).get('name', 'UNKNOWN')
            wep_slots = car_data['weapons_data'].get(wep_key, {}).get('slots', '?') if wep_key else '?'
            # Display 1-based index for user
            mount_line = f"{mount_index+1:<3}{point_name:<15}{point_size:<6}{wep_name:<12}{wep_slots:<6}"

            if mount_y < menu_h - 2 and art_x + len(mount_line) < available_art_width:
                line_attr = curses.color_pair(highlight_pair) | curses.A_BOLD if is_selected else curses.color_pair(text_pair)
                try:
                    # Pad line with spaces to ensure full highlight background
                    padded_line = mount_line.ljust(available_art_width - art_x)
                    menu_win.addstr(mount_y, art_x, padded_line, line_attr)
                except curses.error: pass

                # Draw flashing indicator on car art (only if weapon is selected)
                if is_selected:
                    rel_x = point_info.get("offset_x", 0); rel_y = point_info.get("offset_y", 0)
                    indicator_x = art_x + art_w // 2 + int(rel_x); indicator_y = art_y + art_h // 2 + int(rel_y)
                    # Adjust indicator position slightly based on relative offset for better visuals
                    if rel_x > art_w * 0.3: indicator_x += 1
                    elif rel_x < -art_w * 0.3: indicator_x -= 1
                    if rel_y > art_h * 0.3: indicator_y += 1
                    elif rel_y < -art_h * 0.3: indicator_y -= 1

                    indicator_char = str(mount_index+1) if not flash_on else "●";
                    indicator_attr = curses.A_BOLD | curses.color_pair(particle_pair)
                    if 0 < indicator_y < menu_h -1 and 0 < indicator_x < menu_w -1:
                        try: menu_win.addch(indicator_y, indicator_x, indicator_char, indicator_attr)
                        except curses.error: pass
            mount_y += 1; mount_index += 1

        # --- Footer ---
        # Updated footer to include Left/Right navigation
        footer = "[TAB] Close | [↑/↓] Navigate Vertical | [←/→] Navigate Sections | [ENTER] Select | [ESC] Quit Game"
        if menu_h > 2 and len(footer) < menu_w - 2:
            try: menu_win.addstr(menu_h - 2, (menu_w - len(footer)) // 2, footer)
            except curses.error: pass

        menu_win.attroff(curses.color_pair(text_pair))
        menu_win.refresh()

    except curses.error as e:
        if menu_win:
            try: menu_win.attroff(curses.color_pair(text_pair))
            except: pass
            del menu_win
        print(f"DEBUG: Error drawing menu: {e}", file=sys.stderr)
        return None
    except Exception as e:
        if menu_win: del menu_win
        print(f"DEBUG: Unexpected error in draw_menu: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return None

    return menu_win
