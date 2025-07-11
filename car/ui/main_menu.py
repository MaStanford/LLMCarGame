import curses
from ..common.utils import draw_box
from ..rendering.rendering_queue import rendering_queue
import logging

def draw_main_menu(stdscr, selected_option, color_map):
    """Adds the main menu to the rendering queue."""
    logging.info("UI_MAIN_MENU: Drawing main menu.")
    h, w = stdscr.getmaxyx()
    menu_options = ["New Game", "Load Game", "Settings", "Quit"]
    
    border_color_pair = color_map.get("MENU_BORDER", 0)
    text_color_pair = color_map.get("MENU_TEXT", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)

    border_pair = border_color_pair if 0 <= border_color_pair < curses.COLOR_PAIRS else 0
    text_pair = text_color_pair if 0 <= text_color_pair < curses.COLOR_PAIRS else 0
    highlight_pair = highlight_color_pair if 0 <= highlight_color_pair < curses.COLOR_PAIRS else text_pair

    menu_h = len(menu_options) + 4
    menu_w = 30
    menu_y = (h - menu_h) // 2
    menu_x = (w - menu_w) // 2
    
    draw_box(stdscr, menu_y, menu_x, menu_h, menu_w, "Car RPG", z_index=20)
    
    for i, option in enumerate(menu_options):
        y = menu_y + i + 2
        x = menu_x + (menu_w - len(option)) // 2
        if i == selected_option:
            rendering_queue.add(21, stdscr.addstr, y, x, option, curses.color_pair(highlight_pair) | curses.A_BOLD)
        else:
            rendering_queue.add(21, stdscr.addstr, y, x, option, curses.color_pair(text_pair))
