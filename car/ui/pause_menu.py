import curses
from ..common.utils import draw_box
from ..rendering.rendering_queue import rendering_queue

def draw_pause_menu(stdscr, selected_option, color_map):
    """Adds the pause menu to the rendering queue."""
    h, w = stdscr.getmaxyx()
    menu_options = ["Resume", "Save Game", "Main Menu", "Quit"]
    
    text_color_pair = color_map.get("MENU_TEXT", 0)
    highlight_color_pair = color_map.get("MENU_HIGHLIGHT", 0)
    bg_color_pair = color_map.get("MENU_BACKGROUND", 0)

    menu_h = len(menu_options) + 4
    menu_w = 30
    menu_y = (h - menu_h) // 2
    menu_x = (w - menu_w) // 2
    
    # Use a high z-index to ensure it's drawn on top
    z_index = 100
    
    # Draw background
    for y in range(menu_h):
        for x in range(menu_w):
            rendering_queue.add(z_index, stdscr.addch, menu_y + y, menu_x + x, ' ', curses.color_pair(bg_color_pair))

    draw_box(stdscr, menu_y, menu_x, menu_h, menu_w, "Paused", z_index=z_index + 1)
    
    for i, option in enumerate(menu_options):
        y = menu_y + i + 2
        x = menu_x + (menu_w - len(option)) // 2
        
        attr = curses.A_BOLD if i == selected_option else curses.A_NORMAL
        color = highlight_color_pair if i == selected_option else text_color_pair
        
        rendering_queue.add(z_index + 2, stdscr.addstr, y, x, option, curses.color_pair(color) | attr)


