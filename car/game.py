import curses
import time
import os
import sys
import traceback
import math
import random

from .audio.audio import AudioManager
from .logic.input import handle_input
from .logic.physics import update_physics_and_collisions
from .rendering.renderer import render_game
from .ui.shop import draw_shop_menu
from .logic.shop import Shop
from .data.shops import SHOP_DATA
from .data.game_constants import CUTSCENE_RADIUS
from .logic.quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective
from .logic.save_load import save_game, load_game, get_save_files
from .logic.shop_logic import handle_shop_interaction
from .logic.quest_logic import handle_quest_interaction, update_quests
from .logic.menu_logic import handle_menu
from .logic.pause_menu_logic import handle_pause_menu
from .logic.npcs import handle_npc_interaction
from .data import *
from .logic.boss import Boss
from .data.enemies import ENEMIES_DATA
from .rendering import *
from .ui import *
from .ui.new_game import draw_new_game_menu
from .ui.pause_menu import draw_pause_menu
from .ui.cutscene import play_cutscene, draw_entity_modal
from .ui.entity_modal import update_and_draw_entity_modal
from .ui.notifications import add_notification, draw_notifications
from .world import *
from .world.generation import get_city_name
from .world.world import World
from .game_state import GameState

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
                        # This is a bit of a hack, we should probably have a better way to load state
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
    car_color_names = [name for name in COLOR_PAIRS_DEFS if name.startswith("CAR_")]
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
            preview_angle = (preview_angle + math.pi / 4) % (2 * math.pi)
        elif key == ord('d'):
            preview_angle = (preview_angle - math.pi / 4) % (2 * math.pi)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            chosen_difficulty = DIFFICULTY_LEVELS[selected_difficulty_index]
            difficulty_mods = DIFFICULTY_MODIFIERS[chosen_difficulty]
            break

    world = World(seed=12345)

    # --- Game Setup ---
    stdscr.nodelay(1) # Switch back to non-blocking for game
    stdscr.clear(); stdscr.refresh()

    if car_color_names:
        chosen_car_pair_name = car_color_names[selected_color_index]
        car_color_pair_num = COLOR_PAIR_MAP.get(chosen_car_pair_name, 0)
    else:
        car_color_pair_num = 0

    game_state = GameState(selected_car_index, chosen_difficulty, difficulty_mods, car_color_names, car_color_pair_num)
    
    # --- Game Loop ---
    game_menu_win = None
    menu_sections = ["weapons", "inventory"]

    while True: # Outer loop (allows restarting)
        if game_state.play_again:
            game_state = GameState(selected_car_index, chosen_difficulty, difficulty_mods, car_color_names, car_color_pair_num)
            if game_menu_win: del game_menu_win; game_menu_win = None
            stdscr.nodelay(1); stdscr.clear(); stdscr.refresh()

        # --- Inner Game Loop ---
        while not game_state.game_over:
            h, w = stdscr.getmaxyx()
            game_state.spawn_radius = max(w, h) * 0.7
            game_state.despawn_radius = max(w, h) * 1.2
            game_state.frame += 1
            if game_state.level_up_message_timer > 0:
                game_state.level_up_message_timer -=1
            if game_state.shop_cooldown > 0:
                game_state.shop_cooldown -= 1

            actions = handle_input(stdscr, game_state)
            game_state.actions = actions

            if actions["toggle_menu"]:
                game_state.menu_open = not game_state.menu_open
                if game_state.menu_open:
                    game_state.menu_selected_section_idx = 0
                    game_state.menu_selected_item_idx = 0
                else:
                    if game_menu_win:
                        try: game_menu_win.erase(); game_menu_win.refresh(); del game_menu_win
                        except Exception: pass
                        game_menu_win = None

            if game_state.menu_open:
                handle_menu(stdscr, game_state, COLOR_PAIR_MAP)
                continue # Skip the rest of the game loop
            
            # --- Normal Game Update (Menu is Closed) ---
            if game_menu_win:
                try: del game_menu_win
                except: pass
                game_menu_win = None

            handle_pause_menu(stdscr, game_state, COLOR_PAIR_MAP)
            
            update_physics_and_collisions(game_state, world, audio_manager, stdscr, COLOR_PAIR_MAP)
            render_game(stdscr, game_state, world, COLOR_PAIR_MAP)
            update_and_draw_entity_modal(stdscr, game_state, COLOR_PAIR_MAP)

            handle_shop_interaction(stdscr, game_state, world, COLOR_PAIR_MAP)
            handle_quest_interaction(game_state, world, audio_manager)
            update_quests(game_state, audio_manager)
            
            if game_state.current_durability <= 0:
                play_death_cutscene(stdscr, COLOR_PAIR_MAP)
                game_state.game_over = True
                game_state.game_over_message = "CAR DESTROYED!"
            elif game_state.current_gas <= 0 and game_state.car_speed <= 0.01:
                game_state.game_over = True
                game_state.game_over_message = "OUT OF GAS!"

        stdscr.nodelay(0)
        game_over_win = draw_game_over_menu(stdscr, game_state.game_over_message, COLOR_PAIR_MAP)
        if game_over_win is None: break

        while True:
            gm_key = stdscr.getch()
            if gm_key == ord('p') or gm_key == ord('P'): game_state.play_again = True; break
            elif gm_key == ord('e') or gm_key == ord('E') or gm_key == 27: game_state.play_again = False; break
        if game_over_win: del game_over_win; game_over_win = None
        stdscr.clear(); stdscr.refresh()
        if not game_state.play_again: break
