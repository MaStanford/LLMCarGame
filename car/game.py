import curses
import time
import os
import sys
import traceback
import math
import random

from .audio import AudioManager
from .input import handle_input
from .physics import update_physics_and_collisions
from .rendering.renderer import render_game
from .ui.shop import draw_shop_menu
from .logic.shop import Shop
from .data.shops import SHOP_DATA
from .data.game_constants import CUTSCENE_RADIUS
from .logic.quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective
from .logic.save_load import save_game, load_game, get_save_files
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
                num_weapons = len(game_state.mounted_weapons)
                num_inventory = len(game_state.player_inventory)
                current_section_name = menu_sections[game_state.menu_selected_section_idx]

                if actions["menu_up"]:
                    if current_section_name == "weapons" and num_weapons > 0:
                        game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx - 1) % num_weapons
                    elif current_section_name == "inventory" and num_inventory > 0:
                        game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx - 1) % num_inventory
                elif actions["menu_down"]:
                    if current_section_name == "weapons" and num_weapons > 0:
                        game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx + 1) % num_weapons
                    elif current_section_name == "inventory" and num_inventory > 0:
                        game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx + 1) % num_inventory
                elif actions["menu_left"]:
                    game_state.menu_selected_section_idx = (game_state.menu_selected_section_idx - 1) % len(menu_sections)
                    game_state.menu_selected_item_idx = 0
                elif actions["menu_right"]:
                    game_state.menu_selected_section_idx = (game_state.menu_selected_section_idx + 1) % len(menu_sections)
                    game_state.menu_selected_item_idx = 0
                elif actions["menu_select"]:
                    if current_section_name == "inventory":
                        # Placeholder for inventory item action
                        pass
                    elif current_section_name == "weapons":
                        # Equip/unequip weapon
                        mount_point = list(game_state.attachment_points.keys())[game_state.menu_selected_item_idx]
                        
                        # Unequip
                        if game_state.mounted_weapons.get(mount_point):
                            weapon_key = game_state.mounted_weapons[mount_point]
                            game_state.player_inventory.append({"type": "gun", "name": WEAPONS_DATA[weapon_key]["name"]})
                            del game_state.mounted_weapons[mount_point]
                        # Equip
                        else:
                            for i, item in enumerate(game_state.player_inventory):
                                if item["type"] == "gun":
                                    weapon_key = [k for k, v in WEAPONS_DATA.items() if v["name"] == item["name"]][0]
                                    if WEAPONS_DATA[weapon_key]["slots"] <= game_state.attachment_points[mount_point]["size"]:
                                        game_state.mounted_weapons[mount_point] = weapon_key
                                        game_state.player_inventory.pop(i)
                                        break
                elif actions["menu_back"]:
                    game_state.menu_open = False

                car_stats_for_menu = { "cash": game_state.player_cash, "durability": int(game_state.current_durability), "max_durability": int(game_state.max_durability),
                                       "current_gas": game_state.current_gas, "gas_capacity": int(game_state.gas_capacity), "ammo_counts": game_state.ammo_counts,
                                       "speed": game_state.car_speed, "world_x": game_state.car_world_x, "world_y": game_state.car_world_y,
                                       "inventory": game_state.player_inventory,
                                       "player_level": game_state.player_level, "current_xp": game_state.current_xp, "xp_to_next_level": game_state.xp_to_next_level,
                                       "mounted_weapons": game_state.mounted_weapons,
                                       "weapons_data": WEAPONS_DATA
                                     }

                current_selection = (menu_sections[game_state.menu_selected_section_idx], game_state.menu_selected_item_idx)
                if game_menu_win:
                    try: del game_menu_win
                    except: pass
                game_state.selected_car_data["weapons_data"] = WEAPONS_DATA
                game_state.selected_car_data["menu_art"] = game_state.all_car_art[0]
                grid_x = round(game_state.car_world_x / CITY_SPACING)
                grid_y = round(game_state.car_world_y / CITY_SPACING)
                loc_desc_ui = get_city_name(grid_x, grid_y)
                game_menu_win = draw_inventory_menu(stdscr, game_state.selected_car_data, car_stats_for_menu, loc_desc_ui, game_state.frame, current_selection, COLOR_PAIR_MAP)

                if game_menu_win is None:
                    game_state.menu_open = False
                    try: stdscr.addstr(h-1, 0, "Error: Menu failed to draw!")
                    except: pass
                    stdscr.refresh(); time.sleep(1)

            else: # --- Normal Game Update (Menu is Closed) ---
                if game_menu_win:
                    try: del game_menu_win
                    except: pass
                    game_menu_win = None

                if actions["toggle_pause"]:
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
                                save_game(game_state)
                                add_notification("Game Saved!", color="MENU_HIGHLIGHT")
                            elif selected_pause_option == 2: # Main Menu
                                return
                            elif selected_pause_option == 3: # Quit
                                sys.exit(0)
                        elif key == 27: # ESC also resumes
                            break
                
                update_physics_and_collisions(game_state, world, audio_manager, stdscr, COLOR_PAIR_MAP)
                render_game(stdscr, game_state, world, COLOR_PAIR_MAP)
                update_and_draw_entity_modal(stdscr, game_state, COLOR_PAIR_MAP)

                if game_state.car_speed < 1.0 and game_state.shop_cooldown == 0:
                    grid_x = round(game_state.car_world_x / CITY_SPACING)
                    grid_y = round(game_state.car_world_y / CITY_SPACING)
                    city_buildings = get_buildings_in_city(grid_x, grid_y)
                    for building in city_buildings:
                        if building['x'] <= game_state.car_world_x < building['x'] + building['w'] and \
                           building['y'] <= game_state.car_world_y < building['y'] + building['h']:
                            if building["type"] in SHOP_DATA:
                                shop_data = SHOP_DATA[building["type"]]
                                shop = Shop(shop_data["name"], shop_data["inventory"])
                                selected_item_index = 0
                                active_list = "shop"
                                while True:
                                    player_stats = {
                                        "inventory": game_state.player_inventory,
                                        "cash": game_state.player_cash,
                                        "durability": game_state.current_durability,
                                        "max_durability": game_state.max_durability,
                                        "current_gas": game_state.current_gas,
                                        "gas_capacity": game_state.gas_capacity
                                    }
                                    draw_shop_menu(stdscr, shop, player_stats, selected_item_index, active_list, COLOR_PAIR_MAP)
                                    key = stdscr.getch()
                                    if key == curses.KEY_UP:
                                        if active_list == "shop":
                                            selected_item_index = (selected_item_index - 1) % len(shop.inventory)
                                        else:
                                            selected_item_index = (selected_item_index - 1) % len(game_state.player_inventory)
                                    elif key == curses.KEY_DOWN:
                                        if active_list == "shop":
                                            selected_item_index = (selected_item_index + 1) % len(shop.inventory)
                                        else:
                                            selected_item_index = (selected_item_index + 1) % len(game_state.player_inventory)
                                    elif key == curses.KEY_LEFT:
                                        active_list = "shop"
                                        selected_item_index = 0
                                    elif key == curses.KEY_RIGHT:
                                        active_list = "player"
                                        selected_item_index = 0
                                    elif key == curses.KEY_ENTER or key == 10 or key == 13:
                                        if active_list == "shop":
                                            item_to_buy = shop.inventory[selected_item_index]
                                            if game_state.player_cash >= item_to_buy["price"]:
                                                game_state.player_cash -= item_to_buy["price"]
                                                game_state.player_inventory.append({"type": "item", "name": item_to_buy["item"]})
                                        else:
                                            item_to_sell = game_state.player_inventory[selected_item_index]
                                            game_state.player_cash += item_to_sell.get("price", 0)
                                            game_state.player_inventory.pop(selected_item_index)
                                    elif key == 27:
                                        game_state.shop_cooldown = 100
                                        break
                                break
                            elif building["type"] == "GENERIC" and building["name"] == "City Hall":
                                if not game_state.current_quest:
                                    quest_key = random.choice(list(QUESTS.keys()))
                                    quest_data = QUESTS[quest_key]
                                    
                                    objectives = []
                                    for obj_class, args in quest_data["objectives"]:
                                        objectives.append(obj_class(*args))

                                    game_state.current_quest = Quest(
                                        name=quest_data["name"],
                                        description=quest_data["description"],
                                        objectives=objectives,
                                        rewards=quest_data["rewards"]
                                    )
                                    add_notification(f"New Quest: {game_state.current_quest.name}", color="MENU_HIGHLIGHT")

                                    if "boss" in quest_data:
                                        boss_data = quest_data["boss"]
                                        boss_car_data = next((c for c in CARS_DATA if c["name"] == boss_data["car"]), None)
                                        if boss_car_data:
                                            boss = Boss(boss_data["name"], boss_car_data, boss_data["hp_multiplier"])
                                            boss.x = game_state.car_world_x + random.uniform(-200, 200)
                                            boss.y = game_state.car_world_y + random.uniform(-200, 200)
                                            boss.hp = boss_car_data["durability"] * boss.hp_multiplier
                                            boss.art = boss_car_data["art"]
                                            boss.width, boss.height = get_car_dimensions(boss.art)
                                            game_state.active_bosses[quest_key] = boss
                                            audio_manager.stop_music()
                                            audio_manager.play_music("car/sounds/boss.mid")
                                else:
                                    add_notification("You already have an active quest.", color="UI_LOCATION")
                                break
                
                if game_state.current_durability <= 0:
                    play_death_cutscene(stdscr, COLOR_PAIR_MAP)
                    game_state.game_over = True
                    game_state.game_over_message = "CAR DESTROYED!"
                elif game_state.current_gas <= 0 and game_state.car_speed <= 0.01:
                    game_state.game_over = True
                    game_state.game_over_message = "OUT OF GAS!"

            # --- Quest Update Logic ---
            if game_state.current_quest:
                game_state_for_quest = {
                    "active_bosses": game_state.active_bosses,
                    "active_enemies": game_state.active_enemies,
                }
                game_state.current_quest.update(game_state_for_quest)

                if game_state.current_quest.completed:
                    rewards = game_state.current_quest.rewards
                    game_state.gain_xp(rewards.get("xp", 0))
                    game_state.player_cash += rewards.get("cash", 0)
                    add_notification(f"Quest Complete: {game_state.current_quest.name}", color="MENU_HIGHLIGHT")
                    play_cutscene(stdscr, [[f"Quest Complete!"]], 1)
                    game_state.current_quest = None
                else:
                    for objective in game_state.current_quest.objectives:
                        if isinstance(objective, SurvivalObjective):
                            if objective.timer > 0:
                                spawn_rate_mod = game_state.difficulty_mods["spawn_rate_mult"] * 3.0 
                            elif not objective.mini_boss_spawned:
                                mini_boss_name = objective.mini_boss_name
                                if mini_boss_name in ENEMIES_DATA:
                                    edata_s = ENEMIES_DATA[ENEMIES_DATA.index(next(item for item in ENEMIES_DATA if item["name"] == mini_boss_name))]
                                    eh_s, ew_s = get_obstacle_dimensions(edata_s["art"])
                                    sangle = random.uniform(0, 2*math.pi)
                                    sdist = random.uniform(max(w,h)*0.6, game_state.spawn_radius)
                                    sx = game_state.car_world_x + sdist*math.cos(sangle)
                                    sy = game_state.car_world_y + sdist*math.sin(sangle)
                                    evx_s, evy_s = 0, 0
                                    edur_s = int(edata_s["durability"] * game_state.difficulty_mods["enemy_hp_mult"] * 1.5)
                                    game_state.active_enemies[game_state.next_enemy_id] = [sx, sy, ENEMIES_DATA.index(edata_s), eh_s, ew_s, evx_s, evy_s, edata_s["art"], edur_s]
                                    game_state.next_enemy_id += 1
                                    objective.mini_boss_spawned = True
                                    add_notification(f"A powerful enemy has appeared!", color="ENEMY")

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
