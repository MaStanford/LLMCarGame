import math

def get_car_dimensions(car_art_list):
    """Calculates the height and max width across all directional sprites."""
    if not car_art_list or not car_art_list[0]:
        return 0, 0
    height = len(car_art_list[0])
    max_width = 0
    for art in car_art_list:
        if art:
            current_max_line_width = 0
            for line in art:
                visual_width = 0
                in_escape = False
                for char in line:
                    if char == '<': in_escape = True; continue
                    if char == '>': in_escape = False; continue
                    if not in_escape: visual_width += 1
                current_max_line_width = max(current_max_line_width, visual_width)
            max_width = max(max_width, current_max_line_width)
    return height, max_width

def get_obstacle_dimensions(obstacle_art):
    """Calculates the height and max width of an obstacle's ASCII art."""
    if not obstacle_art: return 0, 0
    height = len(obstacle_art)
    width = 0
    if height > 0:
        # Find the maximum width among all lines in the art
        width = max(len(line) for line in obstacle_art)
    return height, width

def normalize_angle(angle):
    """Normalize angle to be within -pi to pi."""
    # Reduce angle to [0, 2pi)
    angle = angle % (2 * math.pi)
    # Shift to [-pi, pi)
    if angle >= math.pi:
        angle -= 2 * math.pi
    return angle

def draw_box(win, title=""):
    """Draws a box around a curses window."""
    win.box()
    if title:
        win.addstr(0, 2, f" {title} ")
