import curses
from ..data.game_constants import CUTSCENE_RADIUS
from .cutscene import draw_entity_modal
from ..rendering.rendering_queue import rendering_queue
from ..common.utils import draw_box
import random

def update_and_draw_entity_modal(stdscr, game_state, color_map):
    """
    Finds the closest entity (prioritizing bosses) within the CUTSCENE_RADIUS
    and adds its info modal to the rendering queue.
    """
    closest_entity = None
    closest_dist_sq = CUTSCENE_RADIUS**2

    # Prioritize bosses
    for boss in game_state.active_bosses.values():
        dist_sq = (boss.x - game_state.car_world_x)**2 + (boss.y - game_state.car_world_y)**2
        if dist_sq < closest_dist_sq:
            closest_dist_sq = dist_sq
            closest_entity = {
                "name": boss.name,
                "hp": boss.hp,
                "max_hp": boss.max_durability,
                "art": boss.art.get("N"), # Default to North-facing art
                "type": "boss"
            }

    # If no boss is in range, check for the closest enemy
    if not closest_entity:
        for enemy in game_state.active_enemies:
            dist_sq = (enemy.x - game_state.car_world_x)**2 + (enemy.y - game_state.car_world_y)**2
            if dist_sq < closest_dist_sq:
                closest_dist_sq = dist_sq
                art = enemy.art.get("N") if isinstance(enemy.art, dict) else enemy.art
                closest_entity = {
                    "name": enemy.__class__.__name__.replace("_", " ").title(),
                    "hp": enemy.durability,
                    "max_hp": enemy.max_durability,
                    "art": art,
                    "type": "enemy"
                }

    if closest_entity:
        draw_entity_modal(stdscr, closest_entity, color_map, art=closest_entity["art"])

def draw_explosions(stdscr, game_state, color_map):
    """Draws and updates ongoing explosions."""
    h, w = stdscr.getmaxyx()
    explosions_to_remove = []

    for i, explosion in enumerate(game_state.active_explosions):
        elapsed = game_state.frame - explosion["start_time"]
        if elapsed > explosion["duration"]:
            explosions_to_remove.append(i)
            continue

        art = explosion["art"].get("N") if isinstance(explosion["art"], dict) else explosion["art"]
        art_h = len(art)
        art_w = max(len(line) for line in art) if art_h > 0 else 0
        
        win_h = art_h + 4
        win_w = max(40, art_w + 4)
        win_y = h - win_h - 1
        win_x = w - win_w - 1
        z_index = 110 # Higher than entity modal

        # Draw background
        bg_color = color_map.get("MENU_BACKGROUND", 0)
        for y_pos in range(win_h):
            for x_pos in range(win_w):
                rendering_queue.add(z_index, stdscr.addch, win_y + y_pos, win_x + x_pos, ' ', curses.color_pair(bg_color))
        
        draw_box(stdscr, win_y, win_x, win_h, win_w, "BOOM!", z_index=z_index + 1)

        # Animate explosion
        progress = elapsed / explosion["duration"]
        
        for y in range(art_h):
            new_line = ""
            for x, char in enumerate(art[y]):
                if char == ' ':
                    new_line += ' '
                elif random.random() < progress:
                    new_line += random.choice(["*", "💥", "🔥", " "])
                else:
                    new_line += char
            
            art_x = win_x + (win_w - len(new_line)) // 2
            rendering_queue.add(z_index + 2, stdscr.addstr, win_y + 3 + y, art_x, new_line, curses.color_pair(color_map.get("FLAME", 0)))

    for i in sorted(explosions_to_remove, reverse=True):
        del game_state.active_explosions[i]
