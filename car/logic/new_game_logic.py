import curses
import math
from ..ui.new_game import draw_new_game_menu
from ..logic.entity_loader import PLAYER_CARS
from ..data.difficulty import DIFFICULTY_LEVELS, DIFFICULTY_MODIFIERS
from ..data.colors import COLOR_PAIRS_DEFS

def handle_new_game_setup(stdscr, color_map):
    """
    Handles the car and difficulty selection menu.
    Returns a dictionary with the chosen settings for GameState creation.
    """
    selected_car_index = 0
    selected_color_index = 0
    selected_difficulty_index = 1  # Default to Normal
    selected_weapon_index = 0
    preview_angle = 0.0
    car_color_names = [name for name in COLOR_PAIRS_DEFS if name.startswith("CAR_")]

    while True:
        car_class = PLAYER_CARS[selected_car_index]
        car_instance = car_class(0, 0)
        default_weapons = list(car_instance.default_weapons.values())

        draw_new_game_menu(
            stdscr, selected_car_index, selected_color_index, 
            selected_difficulty_index, selected_weapon_index, 
            car_color_names, color_map, preview_angle
        )
        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            selected_car_index = (selected_car_index - 1) % len(PLAYER_CARS)
            selected_weapon_index = 0
        elif key == curses.KEY_RIGHT:
            selected_car_index = (selected_car_index + 1) % len(PLAYER_CARS)
            selected_weapon_index = 0
        elif key == curses.KEY_UP:
            selected_difficulty_index = (selected_difficulty_index - 1) % len(DIFFICULTY_LEVELS)
        elif key == curses.KEY_DOWN:
            selected_difficulty_index = (selected_difficulty_index + 1) % len(DIFFICULTY_LEVELS)
        elif key == ord('c'):
            selected_color_index = (selected_color_index + 1) % len(car_color_names)
        elif key == ord('w'):
            if default_weapons:
                selected_weapon_index = (selected_weapon_index - 1) % len(default_weapons)
        elif key == ord('s'):
            if default_weapons:
                selected_weapon_index = (selected_weapon_index + 1) % len(default_weapons)
        elif key == ord('a'):
            preview_angle = (preview_angle + math.pi / 4) % (2 * math.pi)
        elif key == ord('d'):
            preview_angle = (preview_angle - math.pi / 4) % (2 * math.pi)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            chosen_difficulty = DIFFICULTY_LEVELS[selected_difficulty_index]
            difficulty_mods = DIFFICULTY_MODIFIERS[chosen_difficulty]
            
            chosen_car_pair_name = car_color_names[selected_color_index]
            car_color_pair_num = color_map.get(chosen_car_pair_name, 0)

            return {
                "selected_car_index": selected_car_index,
                "difficulty": chosen_difficulty,
                "difficulty_mods": difficulty_mods,
                "car_color_names": car_color_names,
                "car_color_pair_num": car_color_pair_num,
            }
