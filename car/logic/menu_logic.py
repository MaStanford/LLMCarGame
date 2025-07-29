import curses
import time
import math
from ..data.weapons import WEAPONS_DATA
from ..ui.inventory import draw_inventory_menu
from ..data.game_constants import CITY_SPACING
from ..entities.weapon import Weapon

def handle_menu(stdscr, game_state, color_pair_map):
    """Handles all logic for the inventory menu."""
    if not game_state.menu_open:
        return

    h, w = stdscr.getmaxyx()
    menu_sections = ["weapons", "inventory", "factions"]
    num_weapons = len(game_state.mounted_weapons)
    num_inventory = len(game_state.player_inventory)
    num_factions = len(game_state.faction_reputation)
    current_section_name = menu_sections[game_state.menu_selected_section_idx]

    if game_state.actions["menu_up"]:
        if current_section_name == "weapons" and num_weapons > 0:
            game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx - 1) % num_weapons
        elif current_section_name == "inventory" and num_inventory > 0:
            game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx - 1) % num_inventory
        elif current_section_name == "factions" and num_factions > 0:
            game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx - 1) % num_factions
    elif game_state.actions["menu_down"]:
        if current_section_name == "weapons" and num_weapons > 0:
            game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx + 1) % num_weapons
        elif current_section_name == "inventory" and num_inventory > 0:
            game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx + 1) % num_inventory
        elif current_section_name == "factions" and num_factions > 0:
            game_state.menu_selected_item_idx = (game_state.menu_selected_item_idx + 1) % num_factions
    elif game_state.actions["menu_left"]:
        game_state.menu_selected_section_idx = (game_state.menu_selected_section_idx - 1) % len(menu_sections)
        game_state.menu_selected_item_idx = 0
    elif game_state.actions["menu_right"]:
        game_state.menu_selected_section_idx = (game_state.menu_selected_section_idx + 1) % len(menu_sections)
        game_state.menu_selected_item_idx = 0
    elif game_state.actions["menu_select"]:
        if current_section_name == "inventory":
            # Placeholder for inventory item action
            pass
        elif current_section_name == "weapons":
            mount_point = list(game_state.attachment_points.keys())[game_state.menu_selected_item_idx]
            if game_state.mounted_weapons.get(mount_point):
                weapon = game_state.mounted_weapons[mount_point]
                game_state.player_inventory.append(weapon)
                del game_state.mounted_weapons[mount_point]
            else:
                for i, item in enumerate(game_state.player_inventory):
                    if isinstance(item, Weapon):
                        if item.base_stats["slots"] <= game_state.attachment_points[mount_point]["size"]:
                            game_state.mounted_weapons[mount_point] = item
                            game_state.player_inventory.pop(i)
                            break
    elif game_state.actions["menu_back"]:
        game_state.menu_open = False
    elif game_state.actions["turn_left"]:
        game_state.menu_preview_angle = (game_state.menu_preview_angle - math.pi / 4) % (2 * math.pi)
    elif game_state.actions["turn_right"]:
        game_state.menu_preview_angle = (game_state.menu_preview_angle + math.pi / 4) % (2 * math.pi)
