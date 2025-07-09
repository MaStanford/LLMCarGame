import curses
import math
from car.data.cars import CARS_DATA
from car.rendering.draw_utils import draw_sprite
from car.data.difficulty import DIFFICULTY_LEVELS

def draw_new_game_menu(stdscr, selected_car_index, selected_color_index, selected_difficulty_index, selected_weapon_index, car_color_names, COLOR_PAIR_MAP, preview_angle):
    h, w = stdscr.getmaxyx()
    stdscr.clear()

    # Title
    title = "Create New Game"
    stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

    # Car Selection
    car = CARS_DATA[selected_car_index]
    car_name = car["name"]
    
    positive_preview_angle = preview_angle % (2 * math.pi)
    preview_direction_index = int((positive_preview_angle + math.pi / 8) / (math.pi / 4)) % 8
    car_art = car["art"][preview_direction_index]


    car_win_h = len(car_art) + 4
    car_win_w = max(len(line) for line in car_art) + 4
    car_win_y = 4
    car_win_x = (w - car_win_w) // 2

    car_win = curses.newwin(car_win_h, car_win_w, car_win_y, car_win_x)
    car_win.box()
    car_win.addstr(1, (car_win_w - len(car_name)) // 2, car_name)
    
    # Draw car art
    color_name = car_color_names[selected_color_index]
    color_pair = COLOR_PAIR_MAP.get(color_name, COLOR_PAIR_MAP.get("DEFAULT", 0))
    draw_sprite(car_win, 2, (car_win_w - len(car_art[0])) // 2, car_art, color_pair)

    # Car Stats
    stats_win_h = 10
    stats_win_w = 40
    stats_win_y = car_win_y + car_win_h + 1
    stats_win_x = (w - stats_win_w) // 2

    stats_win = curses.newwin(stats_win_h, stats_win_w, stats_win_y, stats_win_x)
    stats_win.box()
    stats_win.addstr(1, 2, f"HP: {car['hp']}")
    stats_win.addstr(2, 2, f"Durability: {car['durability']}")
    stats_win.addstr(3, 2, f"Gas Capacity: {car['gas_capacity']}")
    stats_win.addstr(4, 2, f"Speed: {car['hp']}")
    stats_win.addstr(5, 2, f"Handling: {car['turn_rate']}")

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
    weapons_win.addstr(1, (weapons_win_w - len("Weapons")) // 2, "Weapons")

    available_weapons = list(car["mounted_weapons"].values())
    if selected_weapon_index >= len(available_weapons):
        selected_weapon_index = len(available_weapons) -1
    if selected_weapon_index < 0:
        selected_weapon_index = 0
    
    if available_weapons:
        weapon_name = available_weapons[selected_weapon_index]
        weapons_win.addstr(2, (weapons_win_w - len(weapon_name)) // 2, f"< {weapon_name} >")

    stdscr.refresh()
    car_win.refresh()
    stats_win.refresh()
    difficulty_win.refresh()
    weapons_win.refresh()

    # Instructions
    instructions = "Left/Right: Car | Up/Down: Difficulty | W/S: Weapon | C: Color | A/D: Rotate | Enter: Confirm"
    stdscr.addstr(h - 2, (w - len(instructions)) // 2, instructions)
