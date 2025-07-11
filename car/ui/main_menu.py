import curses
from ..common.utils import draw_box

def draw_main_menu(stdscr, selected_option, color_map):
    """Draws the main menu."""
    h, w = stdscr.getmaxyx()
    menu_options = ["New Game", "Load Game", "Settings", "Quit"]
    
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
        
        draw_box(menu_win, "Car RPG")
        
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
        print(f"Error drawing main menu: {e}", file=sys.stderr)
        return None
    return menu_win
