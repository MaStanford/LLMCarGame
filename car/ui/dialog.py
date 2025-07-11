import curses
from ..rendering.rendering_queue import rendering_queue
from ..common.utils import draw_box

def draw_dialog_modal(stdscr, text_lines, color_map):
    """
    Adds a non-blocking dialog modal to the rendering queue.
    """
    h, w = stdscr.getmaxyx()
    modal_h = len(text_lines) + 4
    modal_w = max(len(line) for line in text_lines) + 6
    modal_y = h - modal_h - 1
    modal_x = 1

    draw_box(stdscr, modal_y, modal_x, modal_h, modal_w, "Dialog", z_index=100)

    for i, line in enumerate(text_lines):
        rendering_queue.add(101, stdscr.addstr, modal_y + i + 1, modal_x + 2, line, color_map.get("MENU_TEXT", 0))

    rendering_queue.add(101, stdscr.addstr, modal_y + modal_h - 2, modal_x + 2, "(Press any key to continue)", color_map.get("MENU_TEXT", 0))
