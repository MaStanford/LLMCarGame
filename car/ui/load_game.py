import curses

def draw_load_game_menu(stdscr, save_files, selected_option, color_map):
    """Draws the load game menu."""
    h, w = stdscr.getmaxyx()
    
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)

    border_pair = border_color_pair if 0 <= border_color_pair < curses.COLOR_PAIRS else 0
    text_pair = text_color_pair if 0 <= text_color_pair < curses.COLOR_PAIRS else 0
    highlight_pair = highlight_color_pair if 0 <= highlight_color_pair < curses.COLOR_PAIRS else text_pair

    menu_win = None
    try:
        menu_h = len(save_files) + 4
        menu_w = 40
        menu_y = (h - menu_h) // 2
        menu_x = (w - menu_w) // 2
        
        menu_win = curses.newwin(menu_h, menu_w, menu_y, menu_x)
        menu_win.keypad(True)
        menu_win.bkgd(' ', curses.color_pair(text_pair))
        menu_win.erase()
        
        menu_win.attron(curses.color_pair(border_pair))
        menu_win.box()
        menu_win.attroff(curses.color_pair(border_pair))
        
        title = "Load Game"
        menu_win.addstr(1, (menu_w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(text_pair))

        if not save_files:
            menu_win.addstr(2, (menu_w - len("No save files found.")) // 2, "No save files found.", curses.color_pair(text_pair))
        else:
            for i, option in enumerate(save_files):
                y = i + 2
                x = (menu_w - len(option)) // 2
                if i == selected_option:
                    menu_win.addstr(y, x, option, curses.color_pair(highlight_pair) | curses.A_BOLD)
                else:
                    menu_win.addstr(y, x, option, curses.color_pair(text_pair))
        
        menu_win.refresh()
    except curses.error as e:
        if menu_win: del menu_win
        try: stdscr.addstr(h-1, 0, f"Menu draw error: {e}")
        except curses.error: pass
        print(f"Error drawing load game menu: {e}", file=sys.stderr)
        return None
    return menu_win
