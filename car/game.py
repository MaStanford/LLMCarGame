import curses
import math
import random
import sys
from .logic.entity_loader import PLAYER_CARS
from .data.colors import COLOR_PAIRS_DEFS
from .data.factions import FACTION_DATA
from .logic.spawning import spawn_enemy, spawn_fauna, spawn_obstacle
from .logic.boss import Boss
from .logic.pause_menu_logic import handle_pause_menu
from .logic.menu_logic import handle_menu
from .logic.shop_logic import handle_shop_interaction
from .logic.city_hall_logic import handle_city_hall_interaction
from .logic.quest_logic import update_quests
from .ui.entity_modal import update_and_draw_entity_modal, draw_explosions
from .ui.notifications import draw_notifications
from .ui.cutscene import play_death_cutscene
from .ui.game_over import draw_game_over_menu
from .ui.pause_menu import draw_pause_menu
from .rendering import render_game
from .world import World
from .game_state import GameState
from .logic.input import handle_input
from .logic.physics import update_physics_and_collisions
from .audio.audio import AudioManager
from .logic.main_menu_logic import handle_main_menu
from .logic.new_game_logic import handle_new_game_setup
from .rendering.rendering_queue import rendering_queue
from .data.game_constants import CITY_SPACING
from .world.generation import get_city_name
from .ui.inventory import draw_inventory_menu

def main_game(stdscr, logger):
    """Main function to run the game using curses."""
    # --- Initial Setup ---
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)
    h, w = stdscr.getmaxyx()
    try:
        curses.cbreak()
        stdscr.keypad(True)
    except Exception as e:
        logger.error(f"Warning: Could not set cbreak/keypad: {e}")

    # --- Audio Setup ---
    audio_manager = AudioManager()

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

    # --- Game Start ---
    game_state = None
    while game_state is None:
        action, loaded_state = handle_main_menu(stdscr, audio_manager, COLOR_PAIR_MAP)

        if action == 'quit':
            return
        elif action == 'load_game':
            game_state = loaded_state
        elif action == 'new_game':
            new_game_settings = handle_new_game_setup(stdscr, COLOR_PAIR_MAP)
            if new_game_settings:
                game_state = GameState(**new_game_settings)
            else: # User backed out of new game setup
                continue

    world = World(seed=12345) # Or load from game_state if saved

    # --- Main Game Loop ---
    while True:
        if game_state.play_again:
            # This logic might need adjustment depending on how you want to restart
            new_game_settings = handle_new_game_setup(stdscr, COLOR_PAIR_MAP)
            if new_game_settings:
                game_state = GameState(**new_game_settings)
                stdscr.nodelay(1)
                stdscr.clear()
                stdscr.refresh()
            else: # User backed out of new game setup
                break

        # --- Inner Game Loop ---
        while not game_state.game_over:
            h, w = stdscr.getmaxyx()
            game_state.screen_width = w
            game_state.screen_height = h
            game_state.spawn_radius = max(w, h) * 0.7
            game_state.despawn_radius = max(w, h) * 1.2
            game_state.frame += 1
            if game_state.level_up_message_timer > 0:
                game_state.level_up_message_timer -= 1
            if game_state.shop_cooldown > 0:
                game_state.shop_cooldown -= 1
            if game_state.city_hall_cooldown > 0:
                game_state.city_hall_cooldown -= 1
            if game_state.menu_toggle_cooldown > 0:
                game_state.menu_toggle_cooldown -= 1
            if game_state.menu_nav_cooldown > 0:
                game_state.menu_nav_cooldown -= 1

            actions = handle_input(stdscr, game_state)
            game_state.actions = actions

            if actions["toggle_menu"]:
                game_state.menu_open = not game_state.menu_open
            
            if actions["toggle_pause"]:
                game_state.pause_menu_open = not game_state.pause_menu_open

            if not game_state.menu_open and not game_state.pause_menu_open:
                # --- Only update game logic if not in a menu ---
                update_physics_and_collisions(game_state, world, audio_manager, stdscr, COLOR_PAIR_MAP)

                for entity in game_state.all_entities:
                    entity.update(game_state, world)

            # --- Spawning should happen regardless of menus ---
            game_state.enemy_spawn_timer -= 1
            if game_state.enemy_spawn_timer <= 0:
                spawn_enemy(game_state, world)
                game_state.enemy_spawn_timer = random.randint(50, 100)

            game_state.fauna_spawn_timer -= 1
            if game_state.fauna_spawn_timer <= 0:
                spawn_fauna(game_state, world)
                game_state.fauna_spawn_timer = random.randint(50, 100)

            game_state.obstacle_spawn_timer -= 1
            if game_state.obstacle_spawn_timer <= 0:
                spawn_obstacle(game_state, world)
                game_state.obstacle_spawn_timer = random.randint(50, 100)

            stdscr.erase()
            
            render_game(stdscr, game_state, world, COLOR_PAIR_MAP)
            
            if game_state.menu_open:
                handle_menu(stdscr, game_state, COLOR_PAIR_MAP)
            elif game_state.pause_menu_open:
                handle_pause_menu(stdscr, game_state, COLOR_PAIR_MAP)
            
            if game_state.menu_open:
                car_stats_for_menu = {
                    "cash": game_state.player_cash,
                    "durability": int(game_state.current_durability),
                    "max_durability": int(game_state.max_durability),
                    "current_gas": game_state.current_gas,
                    "gas_capacity": int(game_state.gas_capacity),
                    "ammo_counts": game_state.ammo_counts,
                    "speed": game_state.car_speed,
                    "world_x": game_state.car_world_x,
                    "world_y": game_state.car_world_y,
                    "inventory": game_state.player_inventory,
                    "player_level": game_state.player_level,
                    "current_xp": game_state.current_xp,
                    "xp_to_next_level": game_state.xp_to_next_level,
                    "mounted_weapons": game_state.mounted_weapons,
                    "quests": [game_state.current_quest.name] if game_state.current_quest else [],
                    "faction_reputation": game_state.faction_reputation
                }
                current_selection = (game_state.menu_selected_section_idx, game_state.menu_selected_item_idx)
                car_data_for_menu = {
                    "name": game_state.player_car.__class__.__name__.replace('_', ' ').title(),
                    "attachment_points": game_state.attachment_points,
                    "menu_art": game_state.player_car.art,
                    "color_pair": game_state.car_color_pair_num,
                }
                grid_x = round(game_state.car_world_x / CITY_SPACING)
                grid_y = round(game_state.car_world_y / CITY_SPACING)
                loc_desc_ui = get_city_name(grid_x, grid_y)
                draw_inventory_menu(stdscr, car_data_for_menu, car_stats_for_menu, loc_desc_ui, game_state.frame, current_selection, COLOR_PAIR_MAP, game_state.menu_preview_angle)
            elif game_state.pause_menu_open:
                draw_pause_menu(stdscr, game_state.selected_pause_option, COLOR_PAIR_MAP)
            
            update_and_draw_entity_modal(stdscr, game_state, COLOR_PAIR_MAP)
            draw_explosions(stdscr, game_state, COLOR_PAIR_MAP)
            draw_notifications(stdscr, game_state.notifications, COLOR_PAIR_MAP)
            
            rendering_queue.draw(stdscr)

            handle_city_hall_interaction(stdscr, game_state, world, COLOR_PAIR_MAP)
            handle_shop_interaction(stdscr, game_state, world, COLOR_PAIR_MAP)
            update_quests(game_state, audio_manager)

            
            # Check for win/loss conditions
            num_factions = len(FACTION_DATA)
            defeated_factions = sum(1 for f in FACTION_DATA.values() if "Defeated" in f.get("relationships", {}).values())
            
            if defeated_factions >= num_factions - 1:
                game_state.game_over = True
                game_state.game_over_message = "VICTORY! You control the wasteland."

            hostile_factions = sum(1 for rep in game_state.faction_reputation.values() if rep <= -100)
            if hostile_factions >= num_factions:
                game_state.game_over = True
                game_state.game_over_message = "OUTCAST! Hunted by all, you are alone."

            if game_state.player_car.durability <= 0:
                play_death_cutscene(stdscr, COLOR_PAIR_MAP)
                game_state.game_over = True
                game_state.game_over_message = "CAR DESTROYED!"
            elif game_state.player_car.fuel <= 0 and game_state.car_speed <= 0.01:
                game_state.game_over = True
                game_state.game_over_message = "OUT OF GAS!"

        stdscr.nodelay(0)
        game_over_win = draw_game_over_menu(stdscr, game_state.game_over_message, COLOR_PAIR_MAP)
        if game_over_win is None:
            break

        while True:
            gm_key = stdscr.getch()
            if gm_key == ord('p') or gm_key == ord('P'):
                game_state.play_again = True
                break
            elif gm_key == ord('e') or gm_key == ord('E') or gm_key == 27:
                game_state.play_again = False
                break
        
        if not game_state.play_again:
            break
