import curses
import math
from ..logic.entity_loader import PLAYER_CARS
from ..rendering.draw_utils import draw_sprite, draw_weapon_stats_modal
from ..data.difficulty import DIFFICULTY_LEVELS
from ..common.utils import draw_box
from ..rendering.rendering_queue import rendering_queue
import logging

def draw_new_game_menu(stdscr, selected_car_index, selected_color_index, selected_difficulty_index, selected_weapon_index, car_color_names, COLOR_PAIR_MAP, preview_angle, default_weapons):
    """Adds the new game menu to the rendering queue."""
    logging.info("UI_NEW_GAME: Drawing new game menu.")
    h, w = stdscr.getmaxyx()

    # Title
    title = "Create New Game"
    rendering_queue.add(10, stdscr.addstr, 1, (w - len(title)) // 2, title, curses.A_BOLD)

    # Car Selection
    car_class = PLAYER_CARS[selected_car_index]
    car_instance = car_class(0, 0)
    car_name_formatted = car_instance.__class__.__name__.replace("_", " ").title()
    
    positive_preview_angle = preview_angle % (2 * math.pi)
    preview_direction_index = int((positive_preview_angle + math.pi / 8) / (math.pi / 4)) % 8
    
    direction_keys = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    direction = direction_keys[preview_direction_index]
    car_art = car_instance.art[direction]

    car_win_h = len(car_art) + 3
    car_win_w = max(len(line) for line in car_art) + 4
    car_win_y = 2
    car_win_x = (w - car_win_w) // 2

    draw_box(stdscr, car_win_y, car_win_x, car_win_h, car_win_w, z_index=10)
    
    color_name = car_color_names[selected_color_index]
    color_pair = COLOR_PAIR_MAP.get(color_name, COLOR_PAIR_MAP.get("DEFAULT", 0))
    rendering_queue.add(11, draw_sprite, stdscr, car_win_y + 1, car_win_x + (car_win_w - len(car_art[0])) // 2, car_art, color_pair)

    name_y = car_win_y + car_win_h
    rendering_queue.add(10, stdscr.addstr, name_y, (w - len(car_name_formatted)) // 2, car_name_formatted)

    # Car Stats
    stats_win_h = 10
    stats_win_w = 40
    stats_win_y = name_y + 2
    stats_win_x = (w - stats_win_w) // 2

    draw_box(stdscr, stats_win_y, stats_win_x, stats_win_h, stats_win_w, "Stats", z_index=10)
    rendering_queue.add(11, stdscr.addstr, stats_win_y + 1, stats_win_x + 2, f"Durability: {car_instance.durability}")
    rendering_queue.add(11, stdscr.addstr, stats_win_y + 2, stats_win_x + 2, f"Speed: {car_instance.speed}")
    rendering_queue.add(11, stdscr.addstr, stats_win_y + 3, stats_win_x + 2, f"Handling: {car_instance.handling}")
    rendering_queue.add(11, stdscr.addstr, stats_win_y + 4, stats_win_x + 2, f"Braking: {car_instance.braking_power}")
    rendering_queue.add(11, stdscr.addstr, stats_win_y + 5, stats_win_x + 2, f"Fuel: {car_instance.fuel}")

    # Difficulty Selection
    difficulty_win_h = 5
    difficulty_win_w = 40
    difficulty_win_y = stats_win_y + stats_win_h + 1
    difficulty_win_x = (w - difficulty_win_w) // 2
    
    draw_box(stdscr, difficulty_win_y, difficulty_win_x, difficulty_win_h, difficulty_win_w, "Difficulty", z_index=10)
    
    difficulty_text = f"< {DIFFICULTY_LEVELS[selected_difficulty_index]} >"
    rendering_queue.add(11, stdscr.addstr, difficulty_win_y + 2, difficulty_win_x + (difficulty_win_w - len(difficulty_text)) // 2, difficulty_text)

    # Weapon Selection
    weapons_win_h = 10
    weapons_win_w = 40
    weapons_win_y = difficulty_win_y + difficulty_win_h + 1
    weapons_win_x = (w - weapons_win_w) // 2

    draw_box(stdscr, weapons_win_y, weapons_win_x, weapons_win_h, weapons_win_w, "Starting Weapons", z_index=10)

    if default_weapons:
        for i, weapon in enumerate(default_weapons):
            weapon_name = weapon.name.replace('_', ' ').title()
            if i == selected_weapon_index:
                rendering_queue.add(11, stdscr.addstr, weapons_win_y + i + 1, weapons_win_x + 2, f"> {weapon_name}", curses.A_BOLD)
            else:
                rendering_queue.add(11, stdscr.addstr, weapons_win_y + i + 1, weapons_win_x + 2, f"  {weapon_name}")
        
        # Draw weapon stats modal
        selected_weapon = default_weapons[selected_weapon_index]
        modal_h = 5
        modal_w = 30
        modal_y = weapons_win_y
        modal_x = weapons_win_x + weapons_win_w + 1
        draw_weapon_stats_modal(stdscr, modal_y, modal_x, modal_h, modal_w, selected_weapon, COLOR_PAIR_MAP.get("DEFAULT", 0), z_index=20)
    else:
        rendering_queue.add(11, stdscr.addstr, weapons_win_y + 1, weapons_win_x + 2, "None")

    # Instructions
    instructions = "Left/Right: Car | Up/Down: Difficulty | W/S: Weapon | C: Color | A/D: Rotate | Enter: Confirm"
    rendering_queue.add(10, stdscr.addstr, h - 2, (w - len(instructions)) // 2, instructions)
