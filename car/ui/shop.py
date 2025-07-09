import curses

def draw_shop_menu(stdscr, shop_data, player_cash, color_map):
    """Draws the shop menu."""
    h, w = stdscr.getmaxyx()
    
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)

    border_pair = border_color_pair if 0 <= border_color_pair < curses.COLOR_PAIRS else 0
    text_pair = text_color_pair if 0 <= text_color_pair < curses.COLOR_PAIRS else 0
    highlight_pair = highlight_color_pair if 0 <= highlight_color_pair < curses.COLOR_PAIRS else text_pair

    menu_win = None
    try:
        menu_h = 10
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
        
        title = shop_data["name"]
        menu_win.addstr(1, (menu_w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(text_pair))
        
        cash_text = f"Cash: ${player_cash}"
        menu_win.addstr(2, (menu_w - len(cash_text)) // 2, cash_text, curses.color_pair(text_pair))
        
        # Placeholder for shop items
        
        footer = "[B]uy | [S]ell | [E]xit"
        menu_win.addstr(menu_h - 2, (menu_w - len(footer)) // 2, footer, curses.color_pair(text_pair))
        
        menu_win.refresh()
    except curses.error as e:
        if menu_win: del menu_win
        try: stdscr.addstr(h-1, 0, f"Shop draw error: {e}")
        except curses.error: pass
        print(f"Error drawing shop menu: {e}", file=sys.stderr)
        return None
    return menu_win
