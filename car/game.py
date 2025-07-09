import curses
import time
import os
import sys
import traceback
import math
import random

from .audio import AudioManager
from .ui.shop import draw_shop_menu
from .logic.shop import Shop
from .data.shops import SHOP_DATA
from .logic.quests import Quest, KillBossObjective
from .logic.save_load import save_game, load_game, get_save_files
from .logic.npcs import handle_npc_interaction
from .data import *
from .logic.boss import Boss
from .data.bosses import BOSSES
from .common import *
from .rendering import *
from .ui import *
from .ui.new_game import draw_new_game_menu
from .ui.pause_menu import draw_pause_menu
from .ui.cutscene import play_cutscene
from .ui.notifications import add_notification, draw_notifications
from .world import *
from .world.generation import get_city_name
from .world.world import World

def main_game(stdscr):
    """Main function to run the game using curses."""
    # --- Initial Setup ---
    curses.curs_set(0)
    stdscr.nodelay(1) # Start in non-blocking mode for game loop
    stdscr.timeout(50) # Loop delay (milliseconds)
    h, w = stdscr.getmaxyx()
    try:
        curses.cbreak()
        stdscr.keypad(True)
    except Exception as e:
        print(f"Warning: Could not set cbreak/keypad: {e}", file=sys.stderr)

    # --- Color Setup ---
    COLOR_PAIR_MAP = {}
    bg_color = curses.COLOR_BLACK

    if curses.has_colors():
        curses.start_color()
        can_use_default_bg = False
        try:
            curses.use_default_colors()
            bg_color = -1
            curses.init_pair(0, curses.COLOR_WHITE, -1)
            can_use_default_bg = True
        except Exception:
            curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
            bg_color = curses.COLOR_BLACK
            can_use_default_bg = False

        pair_num_counter = 1
        sorted_defs = sorted(COLOR_PAIRS_DEFS.items(), key=lambda item: item[1].get("id", float('inf')))

        for name, definition in sorted_defs:
            if name == "DEFAULT":
                COLOR_PAIR_MAP[name] = 0; continue
            fg = definition.get("fg", curses.COLOR_WHITE)
            pair_bg_def = definition.get("bg")
            pair_bg = pair_bg_def if pair_bg_def is not None else bg_color
            if not (curses.COLOR_BLACK <= fg <= curses.COLORS - 1): fg = curses.COLOR_WHITE
            if pair_bg != -1 and not (curses.COLOR_BLACK <= pair_bg <= curses.COLORS - 1): pair_bg = curses.COLOR_BLACK

            target_id = definition.get("id")
            pair_id_to_use = -1

            if target_id is not None and 0 < target_id < curses.COLOR_PAIRS and target_id not in COLOR_PAIR_MAP.values():
                pair_id_to_use = target_id
            elif pair_num_counter < curses.COLOR_PAIRS:
                current_id = pair_num_counter
                while current_id in COLOR_PAIR_MAP.values() and current_id < curses.COLOR_PAIRS:
                    current_id += 1
                if current_id < curses.COLOR_PAIRS:
                    pair_id_to_use = current_id
                else:
                    COLOR_PAIR_MAP[name] = 0
                    continue
            else:
                COLOR_PAIR_MAP[name] = 0
                continue

            try:
                curses.init_pair(pair_id_to_use, fg, pair_bg)
                COLOR_PAIR_MAP[name] = pair_id_to_use
                if pair_id_to_use >= pair_num_counter:
                    pair_num_counter = pair_id_to_use + 1
                    while pair_num_counter in COLOR_PAIR_MAP.values() and pair_num_counter < curses.COLOR_PAIRS:
                        pair_num_counter += 1
            except curses.error as e:
                COLOR_PAIR_MAP[name] = 0
                if pair_id_to_use == pair_num_counter:
                    pair_num_counter += 1
                    while pair_num_counter in COLOR_PAIR_MAP.values() and pair_num_counter < curses.COLOR_PAIRS:
                        pair_num_counter += 1
    else: # No colors available
        for name in COLOR_PAIRS_DEFS: COLOR_PAIR_MAP[name] = 0
        print("Terminal does not support colors.")

    car_color_names = [name for name in COLOR_PAIRS_DEFS if name.startswith("CAR_")]
    if car_color_names:
        chosen_car_pair_name = random.choice(car_color_names)
        car_color_pair_num = COLOR_PAIR_MAP.get(chosen_car_pair_name, 0)
    else: car_color_pair_num = 0
    obstacle_color_num = COLOR_PAIR_MAP.get("OBSTACLE", 0)
    particle_color_num = COLOR_PAIR_MAP.get("PARTICLE", 0)
    flame_color_num = COLOR_PAIR_MAP.get("FLAME", 0)
    menu_highlight_num = COLOR_PAIR_MAP.get("MENU_HIGHLIGHT", 0)
    building_outline_color_num = COLOR_PAIR_MAP.get("BUILDING_OUTLINE_COLOR", 0)
    fauna_color_num = COLOR_PAIR_MAP.get("FAUNA", 0)
    ui_xp_bar_color_num = COLOR_PAIR_MAP.get("UI_XP_BAR", 0)


    # --- Audio Setup ---
    audio_manager = AudioManager()

    # --- Main Menu ---
    selected_option = 0
    audio_manager.play_music("car/sounds/main_menu.mid")
    while True:
        main_menu_win = draw_main_menu(stdscr, selected_option, COLOR_PAIR_MAP)
        if main_menu_win is None:
            return

        key = stdscr.getch()
        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % 4
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % 4
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if selected_option == 0: # New Game
                audio_manager.stop_music()
                audio_manager.play_music("car/sounds/world.mid")
                break
            elif selected_option == 1: # Load Game
                save_files = get_save_files()
                if not save_files:
                    continue
                
                selected_save_option = 0
                while True:
                    load_game_win = draw_load_game_menu(stdscr, save_files, selected_save_option, COLOR_PAIR_MAP)
                    if load_game_win is None:
                        break
                        
                    key = stdscr.getch()
                    if key == curses.KEY_UP:
                        selected_save_option = (selected_save_option - 1) % len(save_files)
                    elif key == curses.KEY_DOWN:
                        selected_save_option = (selected_save_option + 1) % len(save_files)
                    elif key == curses.KEY_ENTER or key == 10 or key == 13:
                        game_state = load_game(save_files[selected_save_option])
                        # Restore game state
                        player_level = game_state["player_level"]
                        current_xp = game_state["current_xp"]
                        xp_to_next_level = game_state["xp_to_next_level"]
                        car_world_x = game_state["car_world_x"]
                        car_world_y = game_state["car_world_y"]
                        car_angle = game_state["car_angle"]
                        current_durability = game_state["current_durability"]
                        current_gas = game_state["current_gas"]
                        player_cash = game_state["player_cash"]
                        player_inventory = game_state["player_inventory"]
                        mounted_weapons = game_state["mounted_weapons"]
                        ammo_counts = game_state["ammo_counts"]
                        selected_car_index = game_state["selected_car_index"]
                        difficulty_mods = game_state["difficulty_mods"]
                        
                        # Re-initialize some values based on loaded data
                        selected_car_data = CARS_DATA[selected_car_index]
                        all_car_art = selected_car_data["art"]
                        car_height, car_width = get_car_dimensions(all_car_art)
                        base_horsepower = selected_car_data["hp"]
                        base_turn_rate = selected_car_data["turn_rate"]
                        base_max_durability = selected_car_data["durability"]
                        base_gas_capacity = selected_car_data["gas_capacity"]
                        base_braking_power = selected_car_data["braking"]
                        apply_level_bonuses()
                        
                        break
                    elif key == 27: # ESC
                        break
                break
            elif selected_option == 2: # Settings
                # Placeholder for settings logic
                pass
            elif selected_option == 3: # Quit
                return
    
    # --- Car Selection & Difficulty ---
    selected_car_index = 0
    selected_color_index = 0
    selected_difficulty_index = 1  # Default to Normal

    selected_weapon_index = 0
    preview_angle = 0.0
    while True:
        draw_new_game_menu(stdscr, selected_car_index, selected_color_index, selected_difficulty_index, selected_weapon_index, car_color_names, COLOR_PAIR_MAP, preview_angle)
        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            selected_car_index = (selected_car_index - 1) % len(CARS_DATA)
        elif key == curses.KEY_RIGHT:
            selected_car_index = (selected_car_index + 1) % len(CARS_DATA)
        elif key == curses.KEY_UP:
            selected_difficulty_index = (selected_difficulty_index - 1) % len(DIFFICULTY_LEVELS)
        elif key == curses.KEY_DOWN:
            selected_difficulty_index = (selected_difficulty_index + 1) % len(DIFFICULTY_LEVELS)
        elif key == ord('c'):
            selected_color_index = (selected_color_index + 1) % len(car_color_names)
        elif key == ord('w'):
            selected_weapon_index = (selected_weapon_index - 1)
        elif key == ord('s'):
            selected_weapon_index = (selected_weapon_index + 1)
        elif key == ord('a'):
            preview_angle = normalize_angle(preview_angle + math.pi / 4)
        elif key == ord('d'):
            preview_angle = normalize_angle(preview_angle - math.pi / 4)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            chosen_difficulty = DIFFICULTY_LEVELS[selected_difficulty_index]
            difficulty_mods = DIFFICULTY_MODIFIERS[chosen_difficulty]
            break

    world = World(seed=12345)

    # --- Game Setup ---
    stdscr.nodelay(1) # Switch back to non-blocking for game
    stdscr.clear(); stdscr.refresh()

    selected_car_data = CARS_DATA[selected_car_index]
    all_car_art = selected_car_data["art"]
    car_height, car_width = get_car_dimensions(all_car_art)

    # --- Base Stats for Leveling ---
    base_horsepower = selected_car_data["hp"]
    base_turn_rate = selected_car_data["turn_rate"]
    base_max_durability = selected_car_data["durability"]
    base_gas_capacity = selected_car_data["gas_capacity"]
    base_braking_power = selected_car_data["braking"] # Store base braking too

    # --- Effective Stats (modified by level) ---
    # These will be updated by apply_level_bonuses
    horsepower = 0
    turn_rate = 0.0
    max_durability = 0
    gas_capacity = 0
    braking_power = 0 # Effective braking power
    level_damage_modifier = 1.0 # For weapon damage

    # --- XP and Level Variables ---
    player_level = 1
    current_xp = 0
    xp_to_next_level = INITIAL_XP_TO_LEVEL
    level_up_message_timer = 0 # Timer to display "LEVEL UP!" message

    # --- Other Game State Variables ---
    drag_coefficient = selected_car_data["drag"]
    gas_consumption_rate = selected_car_data["gas_consumption"]
    car_world_x = 0.0; car_world_y = 0.0; car_angle = 0.0
    car_velocity_x = 0.0; car_velocity_y = 0.0; car_speed = 0.0
    current_durability = 0 # Will be set by apply_level_bonuses
    current_gas = 0      # Will be set by apply_level_bonuses
    distance_traveled = 0.0; player_cash = 0
    player_inventory = list(selected_car_data.get("inventory", []))
    mounted_weapons = selected_car_data["mounted_weapons"]
    attachment_points = selected_car_data["attachment_points"]
    ammo_counts = { AMMO_BULLET: selected_car_data.get("ammo_bullet", 0),
                    AMMO_HEAVY_BULLET: selected_car_data.get("ammo_heavy_bullet", 0),
                    AMMO_FUEL: selected_car_data.get("ammo_fuel", 0), }
    weapon_cooldowns = {wep_key: 0 for wep_key in WEAPONS_DATA}
    
    # These will be derived from effective horsepower/braking_power
    acceleration_factor = 0.0
    braking_deceleration_factor = 0.0
    max_speed = 0.0
    gas_consumption_scaler = 0.01

    active_obstacles = {}; next_obstacle_id = 0; obstacle_spawn_timer = 0
    spawn_rate_mod = difficulty_mods["spawn_rate_mult"]
    min_obstacle_spawn_time = int(15 / spawn_rate_mod)
    max_obstacle_spawn_time = int(40 / spawn_rate_mod)
    spawn_radius = max(w, h) * 0.7; despawn_radius = max(w, h) * 1.2
    active_particles = []; active_flames = []
    active_pickups = {}; next_pickup_id = 0
    active_fauna = {}; next_fauna_id = 0; fauna_spawn_timer = 0
    player_quests = set()
    active_bosses = {}
    
    # --- Helper function to apply level bonuses ---
    # Nonlocal variables that this function will modify
    nonlocal_vars = {
        "horsepower": horsepower, "turn_rate": turn_rate, "max_durability": max_durability,
        "current_durability": current_durability, "gas_capacity": gas_capacity,
        "current_gas": current_gas, "level_damage_modifier": level_damage_modifier,
        "acceleration_factor": acceleration_factor, "max_speed": max_speed,
        "braking_power": braking_power, "braking_deceleration_factor": braking_deceleration_factor
    }

    def apply_level_bonuses():
        nonlocal horsepower, turn_rate, max_durability, current_durability, gas_capacity, current_gas
        nonlocal level_damage_modifier, acceleration_factor, max_speed, braking_power, braking_deceleration_factor
        
        if player_level > MAX_LEVEL: # Cap level
            # player_level = MAX_LEVEL # This was causing current_xp to not reset properly if already at max
            pass # Allow XP to accumulate but no more stat gain if at max level

        level_bonus_multiplier = 1.0 + (player_level - 1) * LEVEL_STAT_BONUS_PER_LEVEL

        horsepower = base_horsepower * level_bonus_multiplier
        turn_rate = base_turn_rate * level_bonus_multiplier
        braking_power = base_braking_power * level_bonus_multiplier # Apply bonus to braking

        new_max_durability = int(base_max_durability * level_bonus_multiplier)
        durability_increase = new_max_durability - max_durability
        max_durability = new_max_durability
        current_durability = min(max_durability, current_durability + durability_increase) # Heal by the amount increased
        if player_level == 1: current_durability = max_durability # Full heal at start/reset

        new_gas_capacity = int(base_gas_capacity * level_bonus_multiplier)
        gas_increase = new_gas_capacity - gas_capacity
        gas_capacity = new_gas_capacity
        current_gas = min(gas_capacity, current_gas + gas_increase) # Add gained capacity
        if player_level == 1: current_gas = gas_capacity # Full gas at start/reset
        
        level_damage_modifier = level_bonus_multiplier

        # Recalculate derived stats
        acceleration_factor = horsepower / 500.0
        max_speed = horsepower / 4.0
        braking_deceleration_factor = braking_power / 100.0


    apply_level_bonuses() # Apply initial (level 1) stats

    # --- Game Loop ---
    game_over = False; game_over_message = ""; frame = 0
    menu_open = False; play_again = False
    game_menu_win = None
    menu_sections = ["weapons", "inventory"]
    menu_selected_section_idx = 0
    menu_selected_item_idx = 0

    while True: # Outer loop (allows restarting)
        if play_again:
            # Reset XP and Level
            player_level = 1
            current_xp = 0
            xp_to_next_level = INITIAL_XP_TO_LEVEL
            level_up_message_timer = 0

            # Reset car stats to base (will be modified by level 1 bonuses)
            # Note: apply_level_bonuses will handle setting current_durability and current_gas
            max_durability = 0 # Will be reset by apply_level_bonuses
            gas_capacity = 0   # Will be reset by apply_level_bonuses
            apply_level_bonuses() # This resets effective stats to level 1 values and heals

            car_world_x = 0.0; car_world_y = 0.0; car_angle = 0.0
            car_velocity_x = 0.0; car_velocity_y = 0.0; car_speed = 0.0
            distance_traveled = 0.0; player_cash = 0
            player_inventory = list(selected_car_data.get("inventory", []))
            ammo_counts = { AMMO_BULLET: selected_car_data.get("ammo_bullet", 0),
                            AMMO_HEAVY_BULLET: selected_car_data.get("ammo_heavy_bullet", 0),
                            AMMO_FUEL: selected_car_data.get("ammo_fuel", 0), }
            weapon_cooldowns = {wep_key: 0 for wep_key in WEAPONS_DATA}
            active_obstacles = {}; active_particles = []; active_pickups = {}; active_flames = []
            active_fauna = {}
            game_over = False; game_over_message = ""; menu_open = False; play_again = False; frame = 0
            if game_menu_win: del game_menu_win; game_menu_win = None
            stdscr.nodelay(1); stdscr.clear(); stdscr.refresh()
            menu_selected_section_idx = 0; menu_selected_item_idx = 0

        # --- Inner Game Loop ---
        while not game_over:
            collided_obs_ids = []
            pickups_from_collision = []
            frame += 1
            if level_up_message_timer > 0:
                level_up_message_timer -=1

            car_center_world_x = car_world_x + car_width / 2
            car_center_world_y = car_world_y + car_height / 2
            grid_x = round(car_center_world_x / CITY_SPACING)
            grid_y = round(car_center_world_y / CITY_SPACING)
            loc_desc_ui = get_city_name(grid_x, grid_y)

            keys = set()
            key = stdscr.getch()
            while key != -1:
                keys.add(key)
                key = stdscr.getch()

            tab_key_code = 9
            if tab_key_code in keys:
                menu_open = not menu_open
                keys.discard(tab_key_code)
                if menu_open:
                    menu_selected_section_idx = 0
                    menu_selected_item_idx = 0
                    keys.clear()
                else:
                    if game_menu_win:
                        try: game_menu_win.erase(); game_menu_win.refresh(); del game_menu_win
                        except Exception: pass
                        game_menu_win = None

            if menu_open:
                num_weapons = len(selected_car_data['mounted_weapons'])
                num_inventory = len(player_inventory)
                current_section_name = menu_sections[menu_selected_section_idx]

                if curses.KEY_UP in keys:
                    if current_section_name == "weapons" and num_weapons > 0:
                        menu_selected_item_idx = (menu_selected_item_idx - 1) % num_weapons
                    elif current_section_name == "inventory" and num_inventory > 0:
                        menu_selected_item_idx = (menu_selected_item_idx - 1) % num_inventory
                elif curses.KEY_DOWN in keys:
                    if current_section_name == "weapons" and num_weapons > 0:
                        menu_selected_item_idx = (menu_selected_item_idx + 1) % num_weapons
                    elif current_section_name == "inventory" and num_inventory > 0:
                        menu_selected_item_idx = (menu_selected_item_idx + 1) % num_inventory
                elif curses.KEY_LEFT in keys:
                    menu_selected_section_idx = (menu_selected_section_idx - 1) % len(menu_sections)
                    menu_selected_item_idx = 0
                elif curses.KEY_RIGHT in keys:
                    menu_selected_section_idx = (menu_selected_section_idx + 1) % len(menu_sections)
                    menu_selected_item_idx = 0
                elif curses.KEY_ENTER in keys or 10 in keys or 13 in keys:
                    if current_section_name == "inventory":
                        # Placeholder for inventory item action
                        pass
                    elif current_section_name == "weapons":
                        # Equip/unequip weapon
                        mount_point = list(attachment_points.keys())[menu_selected_item_idx]
                        
                        # Unequip
                        if mounted_weapons.get(mount_point):
                            weapon_key = mounted_weapons[mount_point]
                            player_inventory.append({"type": "gun", "name": WEAPONS_DATA[weapon_key]["name"]})
                            del mounted_weapons[mount_point]
                        # Equip
                        else:
                            for i, item in enumerate(player_inventory):
                                if item["type"] == "gun":
                                    weapon_key = [k for k, v in WEAPONS_DATA.items() if v["name"] == item["name"]][0]
                                    if WEAPONS_DATA[weapon_key]["slots"] <= attachment_points[mount_point]["size"]:
                                        mounted_weapons[mount_point] = weapon_key
                                        player_inventory.pop(i)
                                        break
                elif 27 in keys: # ESC key quits game
                    game_over = True; game_over_message = "Game Exited"; play_again = False; continue

                car_stats_for_menu = { "cash": player_cash, "durability": int(current_durability), "max_durability": int(max_durability),
                                       "current_gas": current_gas, "gas_capacity": int(gas_capacity), "ammo_counts": ammo_counts,
                                       "speed": car_speed, "world_x": car_world_x, "world_y": car_world_y,
                                       "inventory": player_inventory,
                                       "player_level": player_level, "current_xp": current_xp, "xp_to_next_level": xp_to_next_level, # XP stats for menu
                                       "quests": player_quests,
                                       "mounted_weapons": mounted_weapons,
                                       "weapons_data": WEAPONS_DATA
                                     }

                current_selection = (menu_sections[menu_selected_section_idx], menu_selected_item_idx)
                if game_menu_win:
                    try: del game_menu_win
                    except: pass
                selected_car_data["weapons_data"] = WEAPONS_DATA
                game_menu_win = draw_inventory_menu(stdscr, selected_car_data, car_stats_for_menu, loc_desc_ui, frame, current_selection, COLOR_PAIR_MAP)

                if game_menu_win is None:
                    menu_open = False
                    try: stdscr.addstr(h-1, 0, "Error: Menu failed to draw!")
                    except: pass
                    stdscr.refresh(); time.sleep(1)

            else: # --- Normal Game Update (Menu is Closed) ---
                if game_menu_win:
                    try: del game_menu_win
                    except: pass
                    game_menu_win = None

                elif 27 in keys: # ESC key opens pause menu
                    selected_pause_option = 0
                    while True:
                        draw_pause_menu(stdscr, selected_pause_option, COLOR_PAIR_MAP)
                        key = stdscr.getch()
                        if key == curses.KEY_UP:
                            selected_pause_option = (selected_pause_option - 1) % 4
                        elif key == curses.KEY_DOWN:
                            selected_pause_option = (selected_pause_option + 1) % 4
                        elif key == curses.KEY_ENTER or key == 10 or key == 13:
                            if selected_pause_option == 0: # Resume
                                break
                            elif selected_pause_option == 1: # Save Game
                                game_state = {
                                    "player_level": player_level,
                                    "current_xp": current_xp,
                                    "xp_to_next_level": xp_to_next_level,
                                    "car_world_x": car_world_x,
                                    "car_world_y": car_world_y,
                                    "car_angle": car_angle,
                                    "current_durability": current_durability,
                                    "current_gas": current_gas,
                                    "player_cash": player_cash,
                                    "player_inventory": player_inventory,
                                    "mounted_weapons": mounted_weapons,
                                    "ammo_counts": ammo_counts,
                                    "selected_car_index": selected_car_index,
                                    "difficulty_mods": difficulty_mods,
                                }
                                save_game(game_state)
                                add_notification("Game Saved!", color="MENU_HIGHLIGHT")
                            elif selected_pause_option == 2: # Main Menu
                                return
                            elif selected_pause_option == 3: # Quit
                                sys.exit(0)
                        elif key == 27: # ESC also resumes
                            break

                accelerate = False; brake = False; turn_left = False; turn_right = False; fire_input = False
                if ord('w') in keys or curses.KEY_UP in keys:
                    accelerate = True
                if ord('s') in keys or curses.KEY_DOWN in keys:
                    brake = True
                if ord('a') in keys or curses.KEY_LEFT in keys:
                    turn_left = True
                if ord('d') in keys or curses.KEY_RIGHT in keys:
                    turn_right = True
                if ord(' ') in keys:
                    fire_input = True
                if curses.KEY_ENTER in keys or 10 in keys or 13 in keys:
                    brake = True

                # --- Update Logic (Physics, Collisions, etc.) ---
                for wep_key in weapon_cooldowns: weapon_cooldowns[wep_key] = max(0, weapon_cooldowns[wep_key] - 1)

                turn_this_frame = 0.0
                speed_turn_modifier = max(0.1, 1.0 - (car_speed / (max_speed * 1.5 if max_speed > 0 else 1.5))) # Avoid div by zero if max_speed is 0
                effective_turn_rate = turn_rate * speed_turn_modifier
                if turn_right: turn_this_frame += effective_turn_rate
                if turn_left: turn_this_frame -= effective_turn_rate
                car_angle = normalize_angle(car_angle + turn_this_frame)

                current_acceleration_force = 0.0; current_braking_force = 0.0
                if accelerate and current_gas > 0: current_acceleration_force = acceleration_factor
                if brake: current_braking_force = braking_deceleration_factor
                
                drag_force = (drag_coefficient * (car_speed**2)) + 0.005
                speed_change = current_acceleration_force - drag_force - current_braking_force
                car_speed += speed_change

                car_center_world_x = car_world_x + car_width / 2; car_center_world_y = car_world_y + car_height / 2
                current_terrain = world.get_terrain_at(car_center_world_x, car_center_world_y)
                terrain_speed_mod = current_terrain.get("speed_modifier", 1.0)
                effective_max_speed = max_speed * terrain_speed_mod
                car_speed = max(0, min(car_speed, effective_max_speed if effective_max_speed > 0 else 0))


                car_velocity_x = car_speed * math.cos(car_angle); car_velocity_y = car_speed * math.sin(car_angle)
                next_world_x = car_world_x + car_velocity_x; next_world_y = car_world_y + car_velocity_y
                next_center_x = next_world_x + car_width / 2; next_center_y = next_world_y + car_height / 2
                next_terrain = world.get_terrain_at(next_center_x, next_center_y)
                if next_terrain.get("passable", True):
                    car_world_x = next_world_x; car_world_y = next_world_y
                else:
                    audio_manager.play_sfx(SFX_MAP["crash"])
                    prev_speed = car_speed; car_speed = 0; car_velocity_x = 0; car_velocity_y = 0
                    current_durability -= max(1, int(prev_speed * 2))
                    audio_manager.play_sfx(SFX_MAP["player_hit"])

                distance_this_frame = car_speed; distance_traveled += distance_this_frame
                gas_used_moving = distance_this_frame * gas_consumption_rate * gas_consumption_scaler
                gas_used_accel = current_acceleration_force * 0.1 if current_acceleration_force > 0 else 0 # Reduced gas for accel
                current_gas = max(0, current_gas - (gas_used_moving + gas_used_accel))

                active_flames.clear()
                if fire_input:
                    for point_name, wep_key in mounted_weapons.items():
                        if weapon_cooldowns[wep_key] <= 0:
                            wep_data = WEAPONS_DATA[wep_key]; ammo_type = wep_data["ammo_type"]
                            if ammo_counts.get(ammo_type, 0) > 0:
                                point_data = attachment_points.get(point_name);
                                if not point_data: continue
                                ammo_counts[ammo_type] -= 1; weapon_cooldowns[wep_key] = wep_data["fire_rate"]
                                offset_x = point_data["offset_x"]; offset_y = point_data["offset_y"]
                                rotated_offset_x = offset_x*math.cos(car_angle) - offset_y*math.sin(car_angle)
                                rotated_offset_y = offset_x*math.sin(car_angle) + offset_y*math.cos(car_angle)
                                forward_proj_offset = car_width * 0.5 + 1.0
                                p_x = car_center_world_x + rotated_offset_x + forward_proj_offset * math.cos(car_angle)
                                p_y = car_center_world_y + rotated_offset_y + forward_proj_offset * math.sin(car_angle)
                                projectile_power = wep_data["power"] * level_damage_modifier # Apply level damage modifier
                                if wep_key == "flamethrower":
                                    end_x = p_x + wep_data["range"]*math.cos(car_angle); end_y = p_y + wep_data["range"]*math.sin(car_angle)
                                    active_flames.append([p_x, p_y, end_x, end_y, projectile_power])
                                    audio_manager.play_sfx(SFX_MAP["flamethrower"])
                                else:
                                    active_particles.append([p_x, p_y, car_angle, wep_data["speed"], projectile_power, wep_data["range"], wep_data["particle"]])
                                    audio_manager.play_sfx(SFX_MAP[wep_key])

                particles_to_remove = []; obstacles_hit_by_projectiles = {}; bosses_hit_by_projectiles = {}
                for i, p_state in enumerate(active_particles):
                    p_x, p_y, p_angle, p_speed, p_power, p_range_left, p_char = p_state
                    p_dist = p_speed; p_x += p_dist*math.cos(p_angle); p_y += p_dist*math.sin(p_angle); p_range_left -= p_dist
                    if p_range_left <= 0: particles_to_remove.append(i); continue
                    collided = False
                    for obs_id, obs_state in active_obstacles.items():
                        ox, oy, _, oh, ow, _, _, _, odur = obs_state
                        if (ox <= p_x < ox + ow and oy <= p_y < oy + oh):
                            obstacles_hit_by_projectiles[obs_id] = obstacles_hit_by_projectiles.get(obs_id, 0) + p_power # p_power already has level_damage_modifier
                            audio_manager.play_sfx(SFX_MAP["enemy_hit"])
                            particles_to_remove.append(i); collided = True; break
                    if collided: continue
                    for boss_id, boss_state in active_bosses.items():
                        bx, by, _, bh, bw, _, _, _, bhp = boss_state
                        if (bx <= p_x < bx + bw and by <= p_y < by + bh):
                            bosses_hit_by_projectiles[boss_id] = bosses_hit_by_projectiles.get(boss_id, 0) + p_power
                            particles_to_remove.append(i); collided = True; break
                    if collided: continue
                    p_terrain = world.get_terrain_at(p_x, p_y)
                    if not p_terrain.get("passable", True):
                        particles_to_remove.append(i); collided = True
                    if not collided: active_particles[i] = [p_x, p_y, p_angle, p_speed, p_power, p_range_left, p_char]

                for fx1, fy1, fx2, fy2, f_power in active_flames: # f_power already has level_damage_modifier
                    flame_len_sq = (fx2-fx1)**2 + (fy2-fy1)**2
                    if flame_len_sq < 1: continue
                    for obs_id, obs_state in active_obstacles.items():
                        ox, oy, _, oh, ow, _, _, _, odur = obs_state
                        ocx = ox + ow/2; ocy = oy + oh/2;
                        flame_min_x = min(fx1, fx2); flame_max_x = max(fx1, fx2)
                        flame_min_y = min(fy1, fy2); flame_max_y = max(fy1, fy2)
                        if (ox < flame_max_x and ox + ow > flame_min_x and
                            oy < flame_max_y and oy + oh > flame_min_y):
                            dist_sq = (ocx-fx1)**2 + (ocy-fy1)**2
                            if dist_sq <= flame_len_sq * 1.1:
                                fdx, fdy = fx2-fx1, fy2-fy1; odx, ody = ocx-fx1, ocy-fy1;
                                dot = fdx*odx + fdy*ody
                                if dot >= 0:
                                    obstacles_hit_by_projectiles[obs_id] = obstacles_hit_by_projectiles.get(obs_id, 0) + f_power
                
                for boss_id, damage in bosses_hit_by_projectiles.items():
                    if boss_id in active_bosses:
                        active_bosses[boss_id].hp -= damage
                        if active_bosses[boss_id].hp <= 0:
                            play_explosion_cutscene(stdscr, active_bosses[boss_id].art[0], COLOR_PAIR_MAP)
                            del active_bosses[boss_id]
                            quest = Quest("kill_boss", "", [KillBossObjective("boss_rick")], {"xp": 1000, "cash": 500})
                            current_xp += quest.rewards["xp"]
                            player_cash += quest.rewards["cash"]
                            play_cutscene(stdscr, [["Quest Complete!"]], 1)
                            player_quests.remove("kill_boss")

                obstacle_ids_to_remove = []; pickups_to_spawn = []
                xp_gained_this_frame = 0 # Track XP for potential level up
                for obs_id, damage in obstacles_hit_by_projectiles.items():
                    if obs_id in active_obstacles:
                        active_obstacles[obs_id][8] -= damage
                        if active_obstacles[obs_id][8] <= 0:
                            obs_state = active_obstacles[obs_id]
                            obs_data = OBSTACLE_DATA[obs_state[2]]
                            play_explosion_cutscene(stdscr, obs_data["art"], COLOR_PAIR_MAP)
                            audio_manager.play_sfx(SFX_MAP["explosion"])
                            obstacle_ids_to_remove.append(obs_id)
                            
                            # Grant XP
                            xp_from_obstacle = obs_data.get("xp_value", 0) * difficulty_mods.get("xp_mult", 1.0)
                            xp_gained_this_frame += int(xp_from_obstacle)

                            if obs_data.get("cash_value", 0) != 0:
                                pk_x = obs_state[0] + obs_state[4]/2 + random.uniform(-0.5, 0.5); pk_y = obs_state[1] + obs_state[3]/2 + random.uniform(-0.5, 0.5)
                                pickups_to_spawn.append([pk_x, pk_y, PICKUP_CASH])
                            drop = obs_data.get("drop_item");
                            if drop and random.random() < obs_data.get("drop_rate", 0):
                                pk_x = obs_state[0] + obs_state[4]/2 + random.uniform(-0.5, 0.5); pk_y = obs_state[1] + obs_state[3]/2 + random.uniform(-0.5, 0.5)
                                pickups_to_spawn.append([pk_x, pk_y, drop])
                            alt_drops = obs_data.get("alt_drop_items")
                            if alt_drops and random.random() < obs_data.get("alt_drop_rate", 0):
                                alt_drop_type = random.choice(alt_drops)
                                pk_x = obs_state[0] + obs_state[4]/2 + random.uniform(-0.5, 0.5); pk_y = obs_state[1] + obs_state[3]/2 + random.uniform(-0.5, 0.5)
                                pickups_to_spawn.append([pk_x, pk_y, alt_drop_type])
                
                # Process XP gain and level up
                if xp_gained_this_frame > 0:
                    current_xp += xp_gained_this_frame
                    while current_xp >= xp_to_next_level and player_level < MAX_LEVEL:
                        current_xp -= xp_to_next_level
                        player_level += 1
                        xp_to_next_level = int(xp_to_next_level * XP_INCREASE_PER_LEVEL_FACTOR)
                        apply_level_bonuses()
                        level_up_message_timer = 60 # Display "LEVEL UP!" for 3 seconds (60 frames * 50ms/frame)
                        play_cutscene(stdscr, [[f"Level Up! You are now level {player_level}"]], 1)
                    if player_level >= MAX_LEVEL: # If max level reached, cap XP at current level's requirement
                        current_xp = min(current_xp, xp_to_next_level -1 if xp_to_next_level > 0 else 0)


                for obs_id in obstacle_ids_to_remove:
                    if obs_id in active_obstacles: del active_obstacles[obs_id]
                unique_indices = sorted(list(set(particles_to_remove)), reverse=True)
                for i in unique_indices:
                    if i < len(active_particles): del active_particles[i]
                for px, py, ptype in pickups_to_spawn:
                    if ptype in PICKUP_DATA:
                        pdata = PICKUP_DATA[ptype]; active_pickups[next_pickup_id] = [px, py, ptype, pdata["art"], pdata["color_pair_name"]]; next_pickup_id += 1

                obstacle_spawn_timer -= 1; ids_to_remove = []
                for obs_id, obs_state in list(active_obstacles.items()):
                    ox, oy, didx, oh, ow, ovx, ovy, oart, odur = obs_state
                    odata = OBSTACLE_DATA[didx]
                    nox = ox + ovx; noy = oy + ovy
                    nterrain = world.get_terrain_at(nox + ow/2, noy + oh/2)
                    if nterrain.get("passable", True):
                        ox, oy = nox, noy
                    else:
                        ovx *= -0.5; ovy *= -0.5
                    if odata["type"] == "moving":
                        dx = car_center_world_x - (ox + ow/2); dy = car_center_world_y - (oy + oh/2); dsq = dx*dx + dy*dy
                        aggro_sq = (spawn_radius*0.8)**2; min_dsq = (car_width+ow)**2
                        if min_dsq < dsq < aggro_sq:
                            dist = math.sqrt(dsq); ovx = (dx/dist)*odata["speed"]; ovy = (dy/dist)*odata["speed"]
                        else:
                            if random.random() < 0.05:
                                wangle = random.uniform(0, 2*math.pi); wspeed = odata["speed"]*0.5; ovx = math.cos(wangle)*wspeed; ovy = math.sin(wangle)*wspeed
                            elif random.random() < 0.1: ovx, ovy = 0, 0
                    active_obstacles[obs_id] = [ox, oy, didx, oh, ow, ovx, ovy, oart, odur]
                    dist_car_sq = (ox - car_world_x)**2 + (oy - car_world_y)**2
                    if dist_car_sq > despawn_radius**2: ids_to_remove.append(obs_id)
                for obs_id in ids_to_remove:
                    if obs_id in active_obstacles: del active_obstacles[obs_id]

                max_obs = 20
                if obstacle_spawn_timer <= 0 and len(active_obstacles) < max_obs:
                    rval = random.random() * TOTAL_SPAWN_RATE; cum_rate = 0; chosen_idx = -1
                    for idx, odata_s in enumerate(OBSTACLE_DATA): # odata_s to avoid conflict
                        cum_rate += odata_s["spawn_rate"]
                        if rval <= cum_rate: chosen_idx = idx; break
                    if chosen_idx != -1:
                        odata_s = OBSTACLE_DATA[chosen_idx]; oh_s, ow_s = get_obstacle_dimensions(odata_s["art"]) # _s suffix
                        attempts = 0
                        while attempts < 10:
                            sangle = random.uniform(0, 2*math.pi); sdist = random.uniform(max(w,h)*0.6, spawn_radius)
                            sx = car_world_x + sdist*math.cos(sangle); sy = car_world_y + sdist*math.sin(sangle)
                            sterrain = world.get_terrain_at(sx + ow_s/2, sy + oh_s/2)
                            if sterrain.get("passable", True):
                                ovx_s, ovy_s = 0, 0 # _s suffix
                                odur_s = int(odata_s["durability"] * difficulty_mods["enemy_hp_mult"]) # _s suffix
                                active_obstacles[next_obstacle_id] = [sx, sy, chosen_idx, oh_s, ow_s, ovx_s, ovy_s, odata_s["art"], odur_s]
                                next_obstacle_id += 1; obstacle_spawn_timer = random.randint(min_obstacle_spawn_time, max_obstacle_spawn_time); break
                            attempts += 1
                        if attempts == 10: obstacle_spawn_timer = min_obstacle_spawn_time
                

                fauna_ids_to_remove = []
                for fauna_id, fauna_state in list(active_fauna.items()):
                    fx, fy, didx, oh, ow, fvx, fvy, fart, fhp = fauna_state
                    fdata = FAUNA_DATA[didx]
                    
                    if fdata["type"] == "hostile":
                        # Move towards player
                        dx = car_world_x - fx
                        dy = car_world_y - fy
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist > 0:
                            fvx = dx / dist * 0.5
                            fvy = dy / dist * 0.5
                    elif fdata["type"] == "neutral":
                        # Wander randomly
                        if random.random() < 0.1:
                            fvx = random.uniform(-0.5, 0.5)
                            fvy = random.uniform(-0.5, 0.5)
                    
                    fx += fvx
                    fy += fvy
                    active_fauna[fauna_id] = [fx, fy, didx, oh, ow, fvx, fvy, fart, fhp]

                    dist_sq = (fx - car_world_x)**2 + (fy - car_world_y)**2
                    if dist_sq < 25 and fdata["type"] == "quest_giver":
                        result = handle_npc_interaction(stdscr, FAUNA_DATA[didx], COLOR_PAIR_MAP)
                        if result == "quest_accepted":
                            player_quests.add("kill_boss")
                        fauna_ids_to_remove.append(fauna_id)

                for fauna_id in fauna_ids_to_remove:
                    if fauna_id in active_fauna: del active_fauna[fauna_id]

                car_hit_w = max(1, car_width-2); car_hit_h = max(1, car_height-2)
                car_scr_cx = w//2; car_scr_cy = h//2;
                car_r1 = car_scr_cx - car_hit_w//2; car_r2 = car_r1 + car_hit_w
                car_ry1 = car_scr_cy - car_hit_h//2; car_ry2 = car_ry1 + car_hit_h
                for obs_id, obs_state in list(active_obstacles.items()):
                    ox, oy, didx, oh, ow, ovx, ovy, oart, odur = obs_state
                    osx = ox - (car_world_x - w/2); osy = oy - (car_world_y - h/2)
                    or1 = int(round(osx)); or2 = or1 + ow; ory1 = int(round(osy)); ory2 = ory1 + oh
                    if (car_r1 < or2 and car_r2 > or1 and car_ry1 < ory2 and car_ry2 > ory1):
                        audio_manager.play_sfx(SFX_MAP["crash"])
                        odata_c = OBSTACLE_DATA[didx]; # _c suffix for collision odata
                        dmg_car = int(odata_c["damage"] * difficulty_mods["enemy_dmg_mult"])
                        speed_f = min(1.0, car_speed/5.0 if car_speed > 0 else 0.0); act_dmg_car = max(1, int(dmg_car * speed_f)); current_durability -= act_dmg_car
                        coll_force = car_speed * selected_car_data["weight"]; dmg_obs = max(1, int(coll_force/5)); active_obstacles[obs_id][8] -= dmg_obs
                        push = 0.5; dx_c = (ox+ow/2) - car_center_world_x; dy_c = (oy+oh/2) - car_center_world_y; dist_c = math.sqrt(dx_c*dx_c + dy_c*dy_c) # _c suffix
                        if dist_c > 0.1: push_vx = (dx_c/dist_c)*push; push_vy = (dy_c/dist_c)*push; active_obstacles[obs_id][5]+=push_vx; active_obstacles[obs_id][6]+=push_vy
                        car_speed *= 0.7
                        if active_obstacles[obs_id][8] <= 0:
                            collided_obs_ids.append(obs_id)
                            # Grant XP for collision kill
                            xp_from_obstacle_coll = odata_c.get("xp_value", 0) * difficulty_mods.get("xp_mult", 1.0)
                            current_xp += int(xp_from_obstacle_coll)
                            # Check for level up immediately after collision kill XP
                            while current_xp >= xp_to_next_level and player_level < MAX_LEVEL:
                                current_xp -= xp_to_next_level
                                player_level += 1
                                xp_to_next_level = int(xp_to_next_level * XP_INCREASE_PER_LEVEL_FACTOR)
                                apply_level_bonuses()
                                level_up_message_timer = 60
                            if player_level >= MAX_LEVEL:
                                current_xp = min(current_xp, xp_to_next_level -1 if xp_to_next_level > 0 else 0)


                            if odata_c.get("cash_value", 0) != 0:
                                pk_x = ox + ow/2 + random.uniform(-0.5, 0.5); pk_y = oy + oh/2 + random.uniform(-0.5, 0.5); pickups_from_collision.append([pk_x, pk_y, PICKUP_CASH])
                            drop = odata_c.get("drop_item");
                            if drop and random.random() < odata_c.get("drop_rate", 0):
                                pk_x = ox + ow/2 + random.uniform(-0.5, 0.5); pk_y = oy + oh/2 + random.uniform(-0.5, 0.5); pickups_from_collision.append([pk_x, pk_y, drop])
                            alt_drops = odata_c.get("alt_drop_items")
                            if alt_drops and random.random() < odata_c.get("alt_drop_rate", 0):
                                alt_drop_type = random.choice(alt_drops)
                                pk_x = ox + ow/2 + random.uniform(-0.5, 0.5); pk_y = oy + oh/2 + random.uniform(-0.5, 0.5); pickups_from_collision.append([pk_x, pk_y, alt_drop_type])

                for obs_id in collided_obs_ids:
                    if obs_id in active_obstacles: del active_obstacles[obs_id]
                for px, py, ptype in pickups_from_collision:
                    if ptype in PICKUP_DATA: pdata=PICKUP_DATA[ptype]; active_pickups[next_pickup_id]=[px, py, ptype, pdata["art"], pdata["color_pair_name"]]; next_pickup_id+=1

                pickups_to_remove = []
                for pid, pstate in list(active_pickups.items()):
                    px, py, ptype, part, pcname = pstate; ph=len(part); pw=len(part[0]) if ph>0 else 0
                    psx = px - (car_world_x - w/2); psy = py - (car_world_y - h/2)
                    pr1=int(round(psx)); pr2=pr1+pw; pry1=int(round(psy)); pry2=pry1+ph
                    if (car_r1 < pr2 and car_r2 > pr1 and car_ry1 < pry2 and car_ry2 > pry1):
                        pinfo = PICKUP_DATA[ptype]; val = pinfo.get("value", 0)
                        if ptype == PICKUP_GAS: current_gas=min(gas_capacity, current_gas+val)
                        elif ptype == PICKUP_REPAIR: current_durability=min(max_durability, current_durability+val)
                        elif ptype == PICKUP_CASH: player_cash += val
                        elif ptype.startswith("AMMO_"):
                            akey = pinfo.get("ammo_type");
                            if akey and akey in ammo_counts: ammo_counts[akey] += val
                        elif ptype.startswith("GUN_"):
                            gun_key = pinfo.get("gun_key")
                            if gun_key:
                                gun_name = WEAPONS_DATA[gun_key]["name"]
                                if not any(item.get("name") == gun_name for item in player_inventory):
                                    player_inventory.append({"type": "gun", "name": gun_name})
                                    add_notification(f"Picked up {gun_name}", color="MENU_HIGHLIGHT")
                        pickups_to_remove.append(pid)
                for pid in pickups_to_remove:
                    if pid in active_pickups: del active_pickups[pid]

                if car_speed < SHOP_INTERACTION_SPEED_THRESHOLD:
                    grid_x = round(car_world_x / CITY_SPACING)
                    grid_y = round(car_world_y / CITY_SPACING)
                    city_buildings = get_buildings_in_city(grid_x, grid_y)
                    for building in city_buildings:
                        if building['x'] <= car_world_x < building['x'] + building['w'] and \
                           building['y'] <= car_world_y < building['y'] + building['h']:
                            if building["type"] in SHOP_DATA:
                                shop_data = SHOP_DATA[building["type"]]
                                shop = Shop(shop_data["name"], shop_data["inventory"])
                                selected_item_index = 0
                                active_list = "shop"
                                while True:
                                    player_stats = {
                                        "inventory": player_inventory,
                                        "cash": player_cash,
                                        "durability": current_durability,
                                        "max_durability": max_durability,
                                        "current_gas": current_gas,
                                        "gas_capacity": gas_capacity
                                    }
                                    draw_shop_menu(stdscr, shop, player_stats, selected_item_index, active_list, COLOR_PAIR_MAP)
                                    key = stdscr.getch()
                                    if key == curses.KEY_UP:
                                        if active_list == "shop":
                                            selected_item_index = (selected_item_index - 1) % len(shop.inventory)
                                        else:
                                            selected_item_index = (selected_item_index - 1) % len(player_inventory)
                                    elif key == curses.KEY_DOWN:
                                        if active_list == "shop":
                                            selected_item_index = (selected_item_index + 1) % len(shop.inventory)
                                        else:
                                            selected_item_index = (selected_item_index + 1) % len(player_inventory)
                                    elif key == curses.KEY_LEFT:
                                        active_list = "shop"
                                        selected_item_index = 0
                                    elif key == curses.KEY_RIGHT:
                                        active_list = "player"
                                        selected_item_index = 0
                                    elif key == curses.KEY_ENTER or key == 10 or key == 13:
                                        if active_list == "shop":
                                            item_to_buy = shop.inventory[selected_item_index]
                                            if player_cash >= item_to_buy["price"]:
                                                player_cash -= item_to_buy["price"]
                                                player_inventory.append({"type": "item", "name": item_to_buy["item"]})
                                        else:
                                            item_to_sell = player_inventory[selected_item_index]
                                            player_cash += item_to_sell.get("price", 0)
                                            player_inventory.pop(selected_item_index)
                                    elif key == 27:
                                        break
                                break
                            elif building["type"] == "GENERIC" and building["name"] == "City Hall":
                                # Accept quest
                                player_quests.add("kill_boss")
                                
                                # Spawn boss
                                boss_data = BOSSES["boss_rick"]
                                boss_car_data = next((c for c in CARS_DATA if c["name"] == boss_data["car"]), None)
                                if boss_car_data:
                                    boss = Boss(boss_data["name"], boss_car_data, boss_data["hp_multiplier"])
                                    boss.x = car_world_x + random.uniform(-200, 200)
                                    boss.y = car_world_y + random.uniform(-200, 200)
                                    boss.hp = boss_car_data["durability"] * boss.hp_multiplier
                                    boss.art = boss_car_data["art"]
                                    boss.width, boss.height = get_car_dimensions(boss.art)
                                    active_bosses["boss_rick"] = boss
                                    audio_manager.stop_music()
                                    audio_manager.play_music("car/sounds/boss.mid")
                                    draw_cutscene_modal(stdscr, f"Boss Encounter: {boss.name}", "Prepare for battle!", COLOR_PAIR_MAP)
                                break
                
                if current_durability <= 0:
                    play_death_cutscene(stdscr, COLOR_PAIR_MAP)
                    game_over = True
                    game_over_message = "CAR DESTROYED!"
                elif current_gas <= 0 and car_speed <= 0.01:
                    game_over = True
                    game_over_message = "OUT OF GAS!"


            # --- Draw ---
            current_city_gx = round(car_world_x / CITY_SPACING)
            current_city_gy = round(car_world_y / CITY_SPACING)
            if (current_city_gx, current_city_gy) != getattr(world, 'last_city', None):
                world.last_city = (current_city_gx, current_city_gy)
                play_cutscene(stdscr, [[f"Entering {get_city_name(current_city_gx, current_city_gy)}"]], 1)

            if not menu_open:
                stdscr.erase()

            world_start_x = car_world_x - w / 2; world_start_y = car_world_y - h / 2
            visible_shop_coords = set()
            visible_buildings = []
            min_gx = math.floor((world_start_x - CITY_SIZE/2) / CITY_SPACING); max_gx = math.ceil((world_start_x + w + CITY_SIZE/2) / CITY_SPACING)
            min_gy = math.floor((world_start_y - CITY_SIZE/2) / CITY_SPACING); max_gy = math.ceil((world_start_y + h + CITY_SIZE/2) / CITY_SPACING)
            for gx_draw in range(min_gx, max_gx + 1): # gx_draw to avoid conflict
                for gy_draw in range(min_gy, max_gy + 1): # gy_draw to avoid conflict
                    buildings_in_city = get_buildings_in_city(gx_draw, gy_draw)
                    for b in buildings_in_city:
                        b_screen_x = b["x"] - world_start_x
                        b_screen_y = b["y"] - world_start_y
                        if b_screen_x + b["w"] > 0 and b_screen_x < w and \
                           b_screen_y + b["h"] > 0 and b_screen_y < h:
                            visible_buildings.append({**b, "sx": b_screen_x, "sy": b_screen_y})
                            if b.get("type") in SHOP_DATA:
                                sinfo = SHOP_DATA[b["type"]]
                                shop_screen_x_start = int(round(b_screen_x))
                                shop_screen_y_start = int(round(b_screen_y))
                                for shop_dy in range(sinfo["height"]):
                                    for shop_dx in range(sinfo["width"]):
                                        sx_shop = shop_screen_x_start + shop_dx # sx_shop
                                        sy_shop = shop_screen_y_start + shop_dy # sy_shop
                                        if 0 <= sx_shop < w and 0 <= sy_shop < h:
                                            visible_shop_coords.add((sx_shop, sy_shop))
            for sy_draw_terrain in range(h): # sy_draw_terrain
                for sx_draw_terrain in range(w): # sx_draw_terrain
                    if (sx_draw_terrain, sy_draw_terrain) in visible_shop_coords:
                        continue
                    cwx = world_start_x + sx_draw_terrain; cwy = world_start_y + sy_draw_terrain
                    terrain = world.get_terrain_at(cwx, cwy)
                    tchar = terrain["char"]
                    tcnum = COLOR_PAIR_MAP.get(terrain["color_pair_name"], 0)
                    pair_num = tcnum if 0 <= tcnum < curses.COLOR_PAIRS else 0
                    try:
                        if sy_draw_terrain < h - 1 or sx_draw_terrain < w - 1:
                            stdscr.addch(sy_draw_terrain, sx_draw_terrain, tchar, curses.color_pair(pair_num))
                    except curses.error: pass

            outline_pair_num = COLOR_PAIR_MAP.get("BUILDING_OUTLINE_COLOR", 0)
            for b in visible_buildings:
                if b.get("type") == "GENERIC":
                    bsx, bsy, bw, bh = int(round(b["sx"])), int(round(b["sy"])), b["w"], b["h"]
                    bname = b.get("name", "")
                    try:
                        stdscr.attron(curses.color_pair(outline_pair_num))
                        if 0 <= bsy < h and 0 <= bsx < w: stdscr.addch(bsy, bsx, BUILDING_OUTLINE["topLeft"])
                        if 0 <= bsy < h and 0 <= bsx + bw - 1 < w: stdscr.addch(bsy, bsx + bw - 1, BUILDING_OUTLINE["topRight"])
                        if 0 <= bsy + bh - 1 < h and 0 <= bsx < w: stdscr.addch(bsy + bh - 1, bsx, BUILDING_OUTLINE["bottomLeft"])
                        if 0 <= bsy + bh - 1 < h and 0 <= bsx + bw - 1 < w: stdscr.addch(bsy + bh - 1, bsx + bw - 1, BUILDING_OUTLINE["bottomRight"])
                        for x_outline in range(bsx + 1, bsx + bw - 1): # x_outline
                            if 0 <= bsy < h and 0 <= x_outline < w: stdscr.addch(bsy, x_outline, BUILDING_OUTLINE["horizontal"])
                            if 0 <= bsy + bh - 1 < h and 0 <= x_outline < w: stdscr.addch(bsy + bh - 1, x_outline, BUILDING_OUTLINE["horizontal"])
                        for y_outline in range(bsy + 1, bsy + bh - 1): # y_outline
                            if 0 <= y_outline < h and 0 <= bsx < w: stdscr.addch(y_outline, bsx, BUILDING_OUTLINE["vertical"])
                            if 0 <= y_outline < h and 0 <= bsx + bw - 1 < w: stdscr.addch(y_outline, bsx + bw - 1, BUILDING_OUTLINE["vertical"])
                        name_y = bsy + 1
                        if 0 <= name_y < h and bh > 2:
                            name_x_start = bsx + 1
                            max_name_w = bw - 2
                            if max_name_w > 0 and len(bname) <= max_name_w:
                                name_draw_x = name_x_start + (max_name_w - len(bname)) // 2
                                if name_draw_x >= bsx + 1:
                                    stdscr.addstr(name_y, name_draw_x, bname)
                    except curses.error: pass
                    finally:
                        try: stdscr.attroff(curses.color_pair(outline_pair_num))
                        except curses.error: pass
            for b in visible_buildings:
                b_type = b.get("type");
                if b_type in SHOP_DATA:
                    sinfo = SHOP_DATA[b_type]; sart = sinfo["art"]; scname = sinfo["color_pair_name"]; scnum = COLOR_PAIR_MAP.get(scname, 0)
                    shop_screen_x = b["sx"]; shop_screen_y = b["sy"]
                    draw_sprite(stdscr, shop_screen_y, shop_screen_x, sart, scnum)

            for oid, ostate in active_obstacles.items():
                ox, oy, didx, oh_obs, ow_obs, _, _, oart, odur = ostate # oh_obs, ow_obs
                osx = ox-world_start_x; osy = oy-world_start_y
                if osx+ow_obs>0 and osx<w and osy+oh_obs>0 and osy<h: draw_sprite(stdscr, osy, osx, oart, obstacle_color_num, transparent_bg=True)
            for fid, fstate in active_fauna.items():
                fx, fy, didx, fh_fauna, fw_fauna, _, _, fart, fhp = fstate
                fsx = fx-world_start_x; fsy = fy-world_start_y
                if fsx+fw_fauna>0 and fsx<w and fsy+fh_fauna>0 and fsy<h: draw_sprite(stdscr, fsy, fsx, fart, fauna_color_num, transparent_bg=True)
            for pid, pstate in active_pickups.items():
                px, py, _, part, pcname = pstate; psx=px-world_start_x; psy=py-world_start_y; pcnum=COLOR_PAIR_MAP.get(pcname,0)
                ph_pickup=len(part); pw_pickup=len(part[0]) if ph_pickup>0 else 0 # ph_pickup, pw_pickup
                if psx+pw_pickup>0 and psx<w and psy+ph_pickup>0 and psy<h: draw_sprite(stdscr, psy, psx, part, pcnum, transparent_bg=True)
            for p_state in active_particles:
                p_x, p_y, _, _, _, _, p_char = p_state
                p_screen_x = p_x - world_start_x; p_screen_y = p_y - world_start_y
                if 0 <= p_screen_x < w and 0 <= p_screen_y < h: draw_sprite(stdscr, p_screen_y, p_screen_x, [p_char], particle_color_num)
            for fx1, fy1, fx2, fy2, _ in active_flames:
                sx1=fx1-world_start_x; sy1=fy1-world_start_y; sx2=fx2-world_start_x; sy2=fy2-world_start_y
                draw_line(stdscr, sy1, sx1, sy2, sx2, FLAME_CHAR, flame_color_num)

            positive_angle = car_angle % (2*math.pi); dir_idx = int((positive_angle + math.pi/8)/(math.pi/4))%8
            if not (0 <= dir_idx < len(all_car_art)): dir_idx = 0
            current_art = all_car_art[dir_idx]
            car_sx = w/2 - car_width/2; car_sy = h/2 - car_height/2
            
            # Get the background character before drawing the car
            bg_char = stdscr.inch(int(car_sy + car_height / 2), int(car_sx + car_width / 2))
            draw_sprite(stdscr, car_sy, car_sx, current_art, car_color_pair_num, transparent_bg=True, bg_char=bg_char)

            # Draw mounted weapons
            for point_name, wep_key in mounted_weapons.items():
                if wep_key:
                    point_data = attachment_points.get(point_name)
                    if point_data:
                        wep_data = WEAPONS_DATA[wep_key]
                        wep_art = wep_data["art"][dir_idx]
                        offset_x = point_data["offset_x"]
                        offset_y = point_data["offset_y"]
                        rotated_offset_x = offset_x * math.cos(car_angle) - offset_y * math.sin(car_angle)
                        rotated_offset_y = offset_x * math.sin(car_angle) + offset_y * math.cos(car_angle)
                        wep_sx = car_sx + car_width / 2 + rotated_offset_x
                        wep_sy = car_sy + car_height / 2 + rotated_offset_y
                        draw_sprite(stdscr, wep_sy, wep_sx, wep_art, car_color_pair_num, transparent_bg=True, bg_char=bg_char)


            # Draw Level Up Message
            if level_up_message_timer > 0:
                lvl_up_msg = "LEVEL UP!"
                msg_x = (w - len(lvl_up_msg)) // 2
                msg_y = h // 2 - car_height // 2 - 2 # Above the car
                if msg_y > 0:
                    try: stdscr.addstr(msg_y, msg_x, lvl_up_msg, curses.A_BOLD | curses.color_pair(COLOR_PAIR_MAP.get("MENU_HIGHLIGHT",0)))
                    except: pass


            if h > 7 and w > 40: # Increased h requirement for more stats
                ctrl1="WASD/Arrows: Steer & Accel/Brake"; ctrl2="SPACE: Fire"; ctrl3="ESC: Quit | TAB: Menu"
                try: stdscr.addstr(0,1,ctrl1); stdscr.addstr(1,1,ctrl2); stdscr.addstr(2,1,ctrl3)
                except curses.error: pass

                loc_line=f"Loc: {loc_desc_ui}"; loc_sc=max(1,(w-len(loc_line))//2)
                loc_color_pair = COLOR_PAIR_MAP.get("UI_LOCATION",0)
                loc_pair = loc_color_pair if 0 <= loc_color_pair < curses.COLOR_PAIRS else 0
                try: stdscr.addstr(0, loc_sc, loc_line, curses.color_pair(loc_pair))
                except curses.error: pass
                
                # ... (compass logic)
                compass_y = 1
                compass_x = w - 20
                if h > 1 and w > 20:
                    if "kill_boss" in player_quests:
                        quest = Quest("kill_boss", "", [KillBossObjective("boss_rick")], {"xp": 1000, "cash": 500})
                        if quest.is_completed({"active_bosses": active_bosses}):
                            player_quests.remove("kill_boss")
                            current_xp += quest.rewards["xp"]
                            player_cash += quest.rewards["cash"]
                            play_cutscene(stdscr, [["Quest Complete!"]], 1)

                if "kill_boss" in player_quests and not active_bosses:
                    boss_data = BOSSES["boss_rick"]
                    boss_car_data = next((c for c in CARS_DATA if c["name"] == boss_data["car"]), None)
                    if boss_car_data:
                        boss = Boss(boss_data["name"], boss_car_data, boss_data["hp_multiplier"])
                        boss.x = car_world_x + random.uniform(-200, 200)
                        boss.y = car_world_y + random.uniform(-200, 200)
                        boss.hp = boss_car_data["durability"] * boss.hp_multiplier
                        boss.art = boss_car_data["art"]
                        boss.width, boss.height = get_car_dimensions(boss.art)
                        active_bosses["boss_rick"] = boss
                        play_cutscene(stdscr, [[f"Boss Encounter: {boss.name}"]], 1)


                if "kill_boss" in player_quests:
                    boss = active_bosses.get("boss_rick")
                    if boss:
                        # Compass
                        angle_to_boss = math.atan2(boss.y - car_world_y, boss.x - car_world_x)
                        angle_diff = normalize_angle(angle_to_boss - car_angle)
                        
                        compass = ""
                        if abs(angle_diff) < math.pi / 8:
                            compass = "↑"
                        elif abs(angle_diff - math.pi) < math.pi / 8:
                            compass = "↓"
                        elif angle_diff > 0:
                            compass = "→"
                        else:
                            compass = "←"
                            
                        stdscr.addstr(1, w - 20, f"Boss: {compass}")

                        # Health Bar
                        boss_hp_p = (boss.hp / (boss.car["durability"] * boss.hp_multiplier)) * 100
                        boss_hp_bl = 20
                        boss_hp_f = int(boss_hp_bl * boss_hp_p / 100)
                        boss_hp_bar = f"[{'█'*boss_hp_f}{'░'*(boss_hp_bl-boss_hp_f)}]"
                        stdscr.addstr(0, w - 40, f"Boss HP: {boss_hp_bar}")

                        # Render Boss
                        boss_sx = boss.x - world_start_x
                        boss_sy = boss.y - world_start_y
                        if boss_sx + boss.width > 0 and boss_sx < w and boss_sy + boss.height > 0 and boss_sy < h:
                            draw_sprite(stdscr, boss_sy, boss_sx, boss.art[0], COLOR_PAIR_MAP.get("OBSTACLE", 0), transparent_bg=True)

                        # Boss modal
                        dist_to_boss = math.sqrt((boss.x - car_world_x)**2 + (boss.y - car_world_y)**2)
                        if dist_to_boss < 50:
                            draw_cutscene_modal(stdscr, f"Boss: {boss.name}", COLOR_PAIR_MAP, persistent=True)

                
                cname=f"Car: {selected_car_data['name']}";
                dur_p=(current_durability/max_durability)*100 if max_durability>0 else 0
                dur_bl=10; dur_f=int(dur_bl*dur_p/100); dur_bar=f"[{'█'*dur_f}{'░'*(dur_bl-dur_f)}]"
                stat1=f"Dur: {dur_bar} {int(current_durability)}/{int(max_durability)}"; # Cast to int for display
                gas_p=(current_gas/gas_capacity)*100 if gas_capacity>0 else 0
                gas_bl=10; gas_f=int(gas_bl*gas_p/100); gas_bar=f"[{'█'*gas_f}{'░'*(gas_bl-gas_f)}]"
                stat2=f"Gas: {gas_bar} {current_gas:.0f}/{int(gas_capacity)}" # Cast to int for display
                stat3=f"Speed: {car_speed:.1f}"; stat4=f"Cash: ${player_cash}";
                ammo_lns=[]
                for pname, wkey in mounted_weapons.items():
                    atype=WEAPONS_DATA[wkey]["ammo_type"]; ammo_lns.append(f"{wkey.upper()}: {ammo_counts.get(atype,0)}")
                ammo_disp=" | ".join(ammo_lns);
                diff_disp = f"Difficulty: {chosen_difficulty}"
                
                # XP and Level UI
                level_disp = f"Level: {player_level}"
                xp_p_ui = (current_xp / xp_to_next_level) * 100 if xp_to_next_level > 0 else 100 # _ui suffix
                xp_bl_ui = 10; xp_f_ui = int(xp_bl_ui * xp_p_ui / 100); # _ui suffix
                xp_bar_str_ui = f"[{'█'*xp_f_ui}{'░'*(xp_bl_ui-xp_f_ui)}]" # _ui suffix
                xp_disp = f"XP: {xp_bar_str_ui} {current_xp}/{xp_to_next_level}"


                all_stats = [cname, stat1, stat2, stat3, stat4, ammo_disp, diff_disp, level_disp, xp_disp] # Added level and XP
                max_len=max(len(s) for s in all_stats) if all_stats else 0
                sc_stats=max(1, w-max_len-1)
                try:
                    for i, stat_line in enumerate(all_stats):
                        if i < h: # Ensure we don't try to draw outside screen height
                            line_color = curses.color_pair(0) # Default color
                            if "XP:" in stat_line: # Color for the XP bar itself
                                # We need to draw the text part and bar part separately if we want different colors
                                # For simplicity, let's color the whole XP line if the bar color is defined
                                if ui_xp_bar_color_num != 0: line_color = curses.color_pair(ui_xp_bar_color_num)
                            stdscr.addstr(i, sc_stats, stat_line, line_color)
                except curses.error: pass

            if not menu_open:
                stdscr.refresh()

            draw_notifications(stdscr, COLOR_PAIR_MAP)

        stdscr.nodelay(0)
        game_over_win = draw_game_over_menu(stdscr, game_over_message, COLOR_PAIR_MAP)
        if game_over_win is None: break

        while True:
            gm_key = stdscr.getch()
            if gm_key == ord('p') or gm_key == ord('P'): play_again = True; break
            elif gm_key == ord('e') or gm_key == ord('E') or gm_key == 27: play_again = False; break
        if game_over_win: del game_over_win; game_over_win = None
        stdscr.clear(); stdscr.refresh()
        if not play_again: break
