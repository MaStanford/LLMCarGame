import curses
import logging
from .rendering_queue import rendering_queue

def draw_sprite(stdscr, y, x, art, color_pair_num, transparent_bg=False, z_index=1):
    """Adds a multi-line ASCII art sprite to the rendering queue."""
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(art):
        for j, char in enumerate(line):
            draw_y, draw_x = int(y + i), int(x + j)
            if (char != ' ' or not transparent_bg) and (0 <= draw_y < h and 0 <= draw_x < w):
                rendering_queue.add(z_index, stdscr.addch, draw_y, draw_x, char, curses.color_pair(color_pair_num))

def draw_line(stdscr, y1, x1, y2, x2, char, color_pair_num, z_index=1):
    """Adds a line of characters to the rendering queue using Bresenham's algorithm."""
    h, w = stdscr.getmaxyx()
    y1, x1, y2, x2 = int(y1), int(x1), int(y2), int(x2)
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    
    while True:
        if 0 <= y1 < h and 0 <= x1 < w:
            rendering_queue.add(z_index, stdscr.addch, y1, x1, char, curses.color_pair(color_pair_num))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:
            err += dx
            y1 += sy

def add_stat_line(stdscr, y, x, label, value, color_pair, z_index=1):
    """Adds a stat line to the rendering queue."""
    h, w = stdscr.getmaxyx()
    if 0 <= y < h and 0 <= x < w:
        rendering_queue.add(z_index, stdscr.addstr, y, x, f"{label}: {value}", color_pair)

def draw_weapon_stats_modal(stdscr, y, x, h, w, weapon, color_pair, z_index=1):
    """Adds a weapon stats modal to the rendering queue."""
    from ..common.utils import draw_box
    draw_box(stdscr, y, x, h, w, weapon.name, z_index)
    add_stat_line(stdscr, y + 1, x + 2, "Damage", weapon.damage, color_pair, z_index + 1)
    add_stat_line(stdscr, y + 2, x + 2, "Range", weapon.range, color_pair, z_index + 1)
    add_stat_line(stdscr, y + 3, x + 2, "Fire Rate", weapon.fire_rate, color_pair, z_index + 1)

def draw_box(stdscr, y, x, h, w, title="", z_index=10):
    """Adds the drawing of a box to the rendering queue."""
    # Draw top and bottom
    for i in range(1, w - 1):
        rendering_queue.add(z_index, stdscr.addch, y, x + i, curses.ACS_HLINE)
        rendering_queue.add(z_index, stdscr.addch, y + h - 1, x + i, curses.ACS_HLINE)
    # Draw sides
    for i in range(1, h - 1):
        rendering_queue.add(z_index, stdscr.addch, y + i, x, curses.ACS_VLINE)
        rendering_queue.add(z_index, stdscr.addch, y + i, x + w - 1, curses.ACS_VLINE)
    # Draw corners
    rendering_queue.add(z_index, stdscr.addch, y, x, curses.ACS_ULCORNER)
    rendering_queue.add(z_index, stdscr.addch, y, x + w - 1, curses.ACS_URCORNER)
    rendering_queue.add(z_index, stdscr.addch, y + h - 1, x, curses.ACS_LLCORNER)
    rendering_queue.add(z_index, stdscr.addch, y + h - 1, x + w - 1, curses.ACS_LRCORNER)
    if title:
        rendering_queue.add(z_index, stdscr.addstr, y, x + 2, f" {title} ")
