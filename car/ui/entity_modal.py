import curses
import time
import random
from ..data.game_constants import CUTSCENE_RADIUS
from .cutscene import draw_entity_modal


def update_and_draw_entity_modal(stdscr, game_state, color_map):
    """
    Finds the closest entity (prioritizing bosses) within the CUTSCENE_RADIUS
    and draws a modal with its information.
    """
    closest_entity = None
    closest_dist_sq = CUTSCENE_RADIUS**2  # Only consider entities within this radius
    boss_in_range = False

    # First, check for the closest boss within range
    for boss_id, boss in game_state.active_bosses.items():
        dist_sq = (boss.x - game_state.car_world_x)**2 + (boss.y - game_state.car_world_y)**2
        if dist_sq < closest_dist_sq:
            closest_dist_sq = dist_sq
            closest_entity = {
                "name": boss.name,
                "hp": boss.hp,
                "max_hp": boss.car_data["durability"] * boss.hp_multiplier,
                "art": boss.art,
                "type": "boss"
            }
            boss_in_range = True

    # If no boss is in range, check for the closest enemy
    if not boss_in_range:
        for enemy in game_state.active_enemies:
            dist_sq = (enemy.x - game_state.car_world_x)**2 + (enemy.y - game_state.car_world_y)**2
            if dist_sq < closest_dist_sq:
                closest_dist_sq = dist_sq
                closest_entity = {
                    "name": enemy.__class__.__name__.replace("_", " ").title(),
                    "hp": enemy.durability,
                    "max_hp": enemy.max_durability,
                    "art": enemy.art,
                    "type": "enemy"
                }

    if closest_entity:
        draw_entity_modal(stdscr, closest_entity, color_map, art=closest_entity["art"])

def play_explosion_in_modal(stdscr, art, color_map):
    """Plays a non-blocking explosion animation inside the entity modal."""
    h, w = stdscr.getmaxyx()
    art_h = len(art)
    art_w = max(len(line) for line in art) if art_h > 0 else 0

    win_h = art_h + 2
    win_w = max(40, art_w + 2)
    win_y = h - win_h - 3
    win_x = w - win_w - 1

    win = curses.newwin(win_h, win_w, win_y, win_x)
    win.bkgd(' ', color_map.get("MENU_BORDER", 0))
    win.box()

    # Initial frame with the enemy art
    for i, line in enumerate(art):
        win.addstr(i + 1, (win_w - len(line)) // 2, line)
    win.refresh()
    time.sleep(0.1)

    # Transition frames
    current_art = [list(row) for row in art]
    for _ in range(art_h * art_w // 4):
        new_art = [row[:] for row in current_art]
        ry, rx = -1, -1
        # Find a non-space character to replace
        for _ in range(20): # Limit attempts to find a character
            ry_t, rx_t = random.randint(0, art_h - 1), random.randint(0, art_w - 1)
            if new_art[ry_t][rx_t] != ' ':
                ry, rx = ry_t, rx_t
                break
        
        if ry != -1:
            new_art[ry][rx] = random.choice(["*", "💥", "🔥"])
            current_art = new_art
        
        for i, row_list in enumerate(current_art):
            win.addstr(i + 1, (win_w - len(row_list)) // 2, "".join(row_list))
        win.refresh()
        time.sleep(0.02)

    # Final explosion frames
    for _ in range(5):
        for i in range(art_h):
            line = "".join(random.choice(["*", "💥", "🔥", " "]) for _ in range(art_w))
            win.addstr(i + 1, (win_w - len(line)) // 2, line)
        win.refresh()
        time.sleep(0.05)
