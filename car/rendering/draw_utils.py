import curses

from .rendering_queue import rendering_queue

def draw_sprite(stdscr, y, x, art, color_pair_num, attributes=0, transparent_bg=False):
    """Draws the specified ASCII art at the given screen coordinates with color and attributes."""
    h, w = stdscr.getmaxyx()
    
    for i, line in enumerate(art):
        draw_y = int(y + i)
        if not (0 <= draw_y < h):
            continue
            
        for j, char in enumerate(line):
            if transparent_bg and char == ' ':
                continue
                
            draw_x = int(x + j)
            if not (0 <= draw_x < w):
                continue

            try:
                # Get the existing character and its attributes at the target location
                bg_char_and_attr = stdscr.inch(draw_y, draw_x)
                
                # The final attribute is a combination of the new color and any other attributes
                final_attr = curses.color_pair(color_pair_num) | attributes
                
                stdscr.addch(draw_y, draw_x, char, final_attr)
            except curses.error:
                pass

def draw_line(stdscr, y1, x1, y2, x2, char, color_pair_num):
    """Draws a line of characters between two points (Bresenham's algorithm)."""
    h, w = stdscr.getmaxyx()
    x1, y1, x2, y2 = int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2))

    dx = abs(x2 - x1); dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1; sy = 1 if y1 < y2 else -1
    err = dx - dy
    x, y = x1, y1
    color_attr = 0
    pair_num = color_pair_num if 0 <= color_pair_num < curses.COLOR_PAIRS else 0
    if curses.has_colors():
        try: color_attr = curses.color_pair(pair_num)
        except: pass

    try:
        if color_attr != 0: stdscr.attron(color_attr)
        count = 0; max_count = w + h
        while count < max_count:
            if 0 <= y < h and 0 <= x < w:
                try:
                    if y < h - 1 or x < w - 1: stdscr.addch(y, x, char)
                except curses.error: pass
            if x == x2 and y == y2: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x += sx
            if e2 < dx: err += dx; y += sy
            count += 1
    finally:
        if color_attr != 0:
            try: stdscr.attroff(color_attr)
            except: pass

def draw_weapon_stats_modal(stdscr, weapon, y, x):
    """Adds a modal with weapon stats to the rendering queue."""
    rendering_queue.add(100, _draw_weapon_stats_modal_internal, weapon, y, x)

def _draw_weapon_stats_modal_internal(stdscr, weapon, y, x):
    """Draws a modal with weapon stats."""
    h, w = stdscr.getmaxyx()
    
    stats = [
        f"Damage: {weapon.damage:.1f}",
        f"Fire Rate: {weapon.fire_rate:.1f}",
        f"Range: {weapon.range:.1f}",
    ]
    if weapon.pellet_count > 1:
        stats.append(f"Pellets: {weapon.pellet_count}")
        
    if weapon.modifiers:
        stats.append("")
        stats.append("Modifiers:")
        for key, value in weapon.modifiers.items():
            stats.append(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            
    win_h = len(stats) + 2
    win_w = max(len(s) for s in stats) + 4
    
    win_y = y - win_h
    win_x = x
    
    if win_y < 0: win_y = y + 1
    if win_x + win_w > w: win_x = w - win_w
    
    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.box()
    
    for i, stat in enumerate(stats):
        win.addstr(i + 1, 2, stat)
        
    win.refresh()

def add_stat_line(win, y, x, text, max_w):
    """Safely draws a line of text into a curses window."""
    max_y, max_x = win.getmaxyx()
    if y < max_y -1 and x < max_x -1 :
        try:
            win.addstr(y, x, text[:max_w])
        except curses.error:
            pass
