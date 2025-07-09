import curses

def draw_sprite(stdscr, y, x, art, color_pair_num, attributes=0, transparent_bg=False, bg_char=None):
    """Draws the specified ASCII art at the given screen coordinates with color and attributes."""
    h, w = stdscr.getmaxyx()
    
    for i, line in enumerate(art):
        draw_y = int(y + i)
        if not (0 <= draw_y < h):
            continue
            
        for j, char in enumerate(line):
            if char == ' ': # Skip spaces for transparency
                continue
                
            draw_x = int(x + j)
            if not (0 <= draw_x < w):
                continue

            try:
                if transparent_bg:
                    # Get the background character and its attributes
                    if bg_char:
                        bg_char_and_attr = bg_char
                    else:
                        bg_char_and_attr = stdscr.inch(draw_y, draw_x)
                    
                    bg_color_pair_number = curses.pair_number(bg_char_and_attr & curses.A_COLOR)
                    fg_color, bg_color = curses.pair_content(bg_color_pair_number)

                    # Create a new color pair with the new foreground and old background
                    new_pair_number = color_pair_num
                    curses.init_pair(new_pair_number, curses.pair_content(color_pair_num)[0], bg_color)
                    
                    final_attr = attributes | curses.color_pair(new_pair_number)
                    stdscr.addch(draw_y, draw_x, char, final_attr)
                else:
                    # Original behavior
                    color_attr = curses.color_pair(color_pair_num) if curses.has_colors() else 0
                    final_attr = color_attr | attributes
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
