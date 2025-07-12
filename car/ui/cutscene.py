import curses
import time
import random
from ..common.utils import draw_box
from ..rendering.rendering_queue import rendering_queue

def play_cutscene(stdscr, frames, delay):
    """Plays a simple cutscene."""
    for frame in frames:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for i, line in enumerate(frame):
            stdscr.addstr(h // 2 - len(frame) // 2 + i, w // 2 - len(line) // 2, line)
        stdscr.refresh()
        time.sleep(delay)

def draw_entity_modal(stdscr, entity, color_map, art=None):
    """Adds an entity modal to the rendering queue."""
    if not entity or entity.get("type") == "static":
        return

    h, w = stdscr.getmaxyx()
    
    art_h = len(art) if art else 0
    art_w = max(len(line) for line in art) if art_h > 0 else 0

    win_h = art_h + 4
    win_w = max(40, art_w + 4)
    win_y = h - win_h - 1
    win_x = w - win_w - 1
    
    z_index = 90 # High z-index for modals

    entity_name = entity.get("name", "Unknown")
    entity_hp = entity.get("hp", 0)
    entity_max_hp = entity.get("max_hp", 100)
    
    # Draw background
    bg_color = color_map.get("MENU_BACKGROUND", 0)
    for y in range(win_h):
        for x in range(win_w):
            rendering_queue.add(z_index, stdscr.addch, win_y + y, win_x + x, ' ', curses.color_pair(bg_color))

    # Draw box and title
    draw_box(stdscr, win_y, win_x, win_h, win_w, entity_name, z_index=z_index + 1)

    # Draw HP bar
    hp_p = (entity_hp / entity_max_hp) * 100 if entity_max_hp > 0 else 0
    hp_bl = win_w - 6
    hp_f = int(hp_bl * hp_p / 100)
    hp_bar_str = f"HP: [{'█'*hp_f}{'░'*(hp_bl-hp_f)}]"
    rendering_queue.add(z_index + 2, stdscr.addstr, win_y + 1, win_x + 2, hp_bar_str, curses.color_pair(color_map.get("MENU_TEXT", 0)))

    # Draw art
    if art:
        art_y = win_y + 3
        for i, line in enumerate(art):
            art_x = win_x + (win_w - len(line)) // 2
            rendering_queue.add(z_index + 2, stdscr.addstr, art_y + i, art_x, line, curses.color_pair(color_map.get("MENU_TEXT", 0)))

def play_death_cutscene(stdscr, color_map):
    """Plays a death cutscene."""
    frames = [
        ["You Died"],
        ["Game Over"],
    ]
    play_cutscene(stdscr, frames, 1)

