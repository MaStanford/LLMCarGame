import curses

def draw_game_over_menu(stdscr, message, color_map):
    """Draws the game over modal."""
    h, w = stdscr.getmaxyx()
    menu_h = 7; menu_w = max(40, len(message) + 6)
    if h < menu_h or w < menu_w:
        try: stdscr.addstr(0, 0, "Screen too small for Game Over!")
        except curses.error: pass
        return None
    menu_y = (h - menu_h) // 2; menu_x = (w - menu_w) // 2
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    border_pair = border_color_pair if 0 <= border_color_pair < curses.COLOR_PAIRS else 0
    text_pair = text_color_pair if 0 <= text_color_pair < curses.COLOR_PAIRS else 0

    menu_win = None
    try:
        menu_win = curses.newwin(menu_h, menu_w, menu_y, menu_x)
        menu_win.bkgd(' ', curses.color_pair(text_pair))
        menu_win.erase()
        menu_win.attron(curses.color_pair(border_pair)); menu_win.box(); menu_win.attroff(curses.color_pair(border_pair))
        menu_win.attron(curses.color_pair(text_pair))
        msg1 = "GAME OVER!"; menu_win.addstr(1, (menu_w - len(msg1)) // 2, msg1, curses.A_BOLD)
        menu_win.addstr(2, (menu_w - len(message)) // 2, message)
        msg3 = "[P]lay Again | [E]xit"; menu_win.addstr(4, (menu_w - len(msg3)) // 2, msg3)
        menu_win.attroff(curses.color_pair(text_pair))
        menu_win.refresh()
    except curses.error as e:
        if menu_win: del menu_win
        try: stdscr.addstr(h-1, 0, f"Game Over draw error: {e}")
        except curses.error: pass
        print(f"Error drawing game over menu: {e}", file=sys.stderr)
        return None
    return menu_win
