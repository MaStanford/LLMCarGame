import curses

def draw_pause_menu(stdscr, selected_option, color_map):
    """Draws the pause menu."""
    h, w = stdscr.getmaxyx()
    menu_options = ["Resume", "Save Game", "Main Menu", "Quit"]
    
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)

    border_pair = border_color_pair if 0 <= border_color_pair < curses.COLOR_PAIRS else 0
    text_pair = text_color_pair if 0 <= text_color_pair < curses.COLOR_PAIRS else 0
    highlight_pair = highlight_color_pair if 0 <= highlight_color_pair < curses.COLOR_PAIRS else text_pair

    menu_win = None
    try:
        menu_h = len(menu_options) + 4
        menu_w = 30
        menu_y = (h - menu_h) // 2
        menu_x = (w - menu_w) // 2
        
        menu_win = curses.newwin(menu_h, menu_w, menu_y, menu_x)
        menu_win.keypad(True)
        menu_win.bkgd(' ', curses.color_pair(text_pair))
        menu_win.erase()
        
        menu_win.attron(curses.color_pair(border_pair))
        menu_win.box()
        menu_win.attroff(curses.color_pair(border_pair))
        
        title = "Paused"
        menu_win.addstr(1, (menu_w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(text_pair))

        for i, option in enumerate(menu_options):
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
        print(f"Error drawing pause menu: {e}", file=sys.stderr)
        return None
    return menu_win
