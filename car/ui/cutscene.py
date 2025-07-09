import curses
import time
import random

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
    """Draws a modal for a game entity, optionally with art."""
    if entity and entity.get("type") == "static":
        return None

    h, w = stdscr.getmaxyx()
    
    art_h = len(art) if art else 0
    art_w = max(len(line) for line in art) if art_h > 0 else 0

    win_h = art_h + 2
    win_w = max(40, art_w + 2)
    win_y = h - win_h - 3
    win_x = w - win_w - 1

    if entity:
        entity_name = entity.get("name", "Unknown")
        entity_hp = entity.get("hp", 0)
        entity_max_hp = entity.get("max_hp", 100)
        
        # Draw name and HP above the box
        stdscr.addstr(win_y - 2, win_x + (win_w - len(entity_name)) // 2, entity_name, curses.A_BOLD)
        
        hp_p = (entity_hp / entity_max_hp) * 100 if entity_max_hp > 0 else 0
        hp_bl = 20
        hp_f = int(hp_bl * hp_p / 100)
        hp_bar = f"HP: [{'█'*hp_f}{'░'*(hp_bl-hp_f)}]"
        stdscr.addstr(win_y - 1, win_x + (win_w - len(hp_bar)) // 2, hp_bar)


    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.bkgd(' ', color_map.get("MENU_BORDER", 0))
    win.box()

    if art:
        for i, line in enumerate(art):
            win.addstr(i + 1, (win_w - len(line)) // 2, line)

    win.refresh()
    return win

def play_death_cutscene(stdscr, color_map):
    """Plays a death cutscene."""
    frames = [
        ["You Died"],
        ["Game Over"],
    ]
    play_cutscene(stdscr, frames, 1)
