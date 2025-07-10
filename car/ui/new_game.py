import curses
import math
import importlib
from ..logic.entity_loader import PLAYER_CARS
from ..rendering.draw_utils import draw_sprite
from ..data.difficulty import DIFFICULTY_LEVELS

def draw_new_game_menu(stdscr, selected_car_index, selected_color_index, selected_difficulty_index, selected_weapon_index, car_color_names, COLOR_PAIR_MAP, preview_angle):
    h, w = stdscr.getmaxyx()
    stdscr.clear()

    # Title
    title = "Create New Game"
    stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

    # Car Selection
    car_class = PLAYER_CARS[selected_car_index]
    car_instance = car_class(0, 0)
    car_name_formatted = car_instance.__class__.__name__.replace("_", " ").title()
    
    
    positive_preview_angle = preview_angle % (2 * math.pi)
    preview_direction_index = int((positive_preview_angle + math.pi / 8) / (math.pi / 4)) % 8
    
    # Get the correct art for the direction
    direction_keys = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    direction = direction_keys[preview_direction_index]
    car_art = car_instance.art[direction]

    car_win_h = len(car_art) + 3
    car_win_w = max(len(line) for line in car_art) + 4
    car_win_y = 2
    car_win_x = (w - car_win_w) // 2

    car_win = curses.newwin(car_win_h, car_win_w, car_win_y, car_win_x)
    car_win.box()
    
    # Draw car art
    color_name = car_color_names[selected_color_index]
    color_pair = COLOR_PAIR_MAP.get(color_name, COLOR_PAIR_MAP.get("DEFAULT", 0))
    draw_sprite(car_win, 1, (car_win_w - len(car_art[0])) // 2, car_art, color_pair)

    # Draw car name below the box
    name_y = car_win_y + car_win_h
    stdscr.addstr(name_y, (w - len(car_name_formatted)) // 2, car_name_formatted)

    # Car Stats
    stats_win_h = 10
    stats_win_w = 40
    stats_win_y = name_y + 2 # Adjusted for the name
    stats_win_x = (w - stats_win_w) // 2

    stats_win = curses.newwin(stats_win_h, stats_win_w, stats_win_y, stats_win_x)
    stats_win.box()
    stats_win.addstr(1, 2, f"Durability: {car_instance.durability}")
    stats_win.addstr(2, 2, f"Speed: {car_instance.speed}")
    stats_win.addstr(3, 2, f"Handling: {car_instance.handling}")
    stats_win.addstr(4, 2, f"Braking: {car_instance.braking_power}")
    stats_win.addstr(5, 2, f"Fuel: {car_instance.fuel}")


    # Difficulty Selection
    difficulty_win_h = 5
    difficulty_win_w = 40
    difficulty_win_y = stats_win_y + stats_win_h + 1
    difficulty_win_x = (w - difficulty_win_w) // 2
    
    difficulty_win = curses.newwin(difficulty_win_h, difficulty_win_w, difficulty_win_y, difficulty_win_x)
    difficulty_win.box()
    difficulty_win.addstr(1, (difficulty_win_w - len("Difficulty")) // 2, "Difficulty")
    
    difficulty_text = f"< {DIFFICULTY_LEVELS[selected_difficulty_index]} >"
    difficulty_win.addstr(2, (difficulty_win_w - len(difficulty_text)) // 2, difficulty_text)

    # Weapon Selection
    weapons_win_h = 10
    weapons_win_w = 40
    weapons_win_y = difficulty_win_y + difficulty_win_h + 1
    weapons_win_x = (w - weapons_win_w) // 2

    weapons_win = curses.newwin(weapons_win_h, weapons_win_w, weapons_win_y, weapons_win_x)
    weapons_win.box()
    weapons_win.addstr(1, (weapons_win_w - len("Starting Weapon")) // 2, "Starting Weapon")

    default_weapons = list(car_instance.default_weapons.values())
    if selected_weapon_index >= len(default_weapons):
        selected_weapon_index = len(default_weapons) -1
    if selected_weapon_index < 0:
        selected_weapon_index = 0
    
    if default_weapons:
        weapon_name = default_weapons[selected_weapon_index]
        weapons_win.addstr(2, (weapons_win_w - len(weapon_name)) // 2, f"< {weapon_name.replace('_', ' ').title()} >")
    else:
        weapons_win.addstr(2, (weapons_win_w - len("None")) // 2, "None")

    stdscr.refresh()
    car_win.refresh()
    stats_win.refresh()
    difficulty_win.refresh()
    weapons_win.refresh()

    # Instructions
    instructions = "Left/Right: Car | Up/Down: Difficulty | W/S: Weapon | C: Color | A/D: Rotate | Enter: Confirm"
    stdscr.addstr(h - 2, (w - len(instructions)) // 2, instructions)
