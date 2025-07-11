import curses
from ..ui.city_hall import draw_city_hall_menu, draw_quest_briefing
from ..ui.dialog import draw_dialog_modal
from ..data.city_info import CITY_INFO
from .quests import QUEST_TEMPLATES
from ..data.factions import FACTION_DATA
from ..world.generation import get_city_faction
import random

from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city
from ..data.buildings import BUILDING_DATA

from ..rendering.rendering_queue import rendering_queue

from .collision_detection import find_safe_exit_spot

def handle_city_hall_interaction(stdscr, game_state, world, color_map):
    """
    Handles the player's interaction with a City Hall, including viewing quests and town info.
    """
    if game_state.car_speed > 1.0 or game_state.city_hall_cooldown != 0:
        return False

    grid_x = round(game_state.car_world_x / CITY_SPACING)
    grid_y = round(game_state.car_world_y / CITY_SPACING)
    city_buildings = get_buildings_in_city(grid_x, grid_y)

    for building in city_buildings:
        if building['type'] == 'city_hall' and \
           building['x'] <= game_state.car_world_x < building['x'] + building['w'] and \
           building['y'] <= game_state.car_world_y < building['y'] + building['h']:
            
            selected_option = 0
            menu_options = ["View Contracts", "Ask about this town", "Leave"]
            
            draw_dialog_modal(stdscr, ["Welcome to the City Hall."], color_map)
            stdscr.nodelay(0)
            stdscr.getch()
            stdscr.nodelay(1)

            while True:
                stdscr.erase()
                draw_city_hall_menu(stdscr, menu_options, selected_option, game_state, color_map)
                rendering_queue.draw(stdscr)
                key = stdscr.getch()

                if key == curses.KEY_UP or key == ord('w'):
                    selected_option = (selected_option - 1) % len(menu_options)
                elif key == curses.KEY_DOWN or key == ord('s'):
                    selected_option = (selected_option + 1) % len(menu_options)
                elif key == 27: # ESC
                    game_state.city_hall_cooldown = 100
                    game_state.car_world_x, game_state.car_world_y = find_safe_exit_spot(world, building)
                    return True
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if selected_option == 0: # View Contracts
                        # Generate a quest
                        quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
                        quest_giver_faction = FACTION_DATA[quest_giver_faction_id]
                        hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
                        if not hostile_factions:
                            draw_dialog_modal(stdscr, ["No available contracts at this time."])
                            stdscr.getch()
                            continue
                        
                        target_faction_id = random.choice(hostile_factions)
                        target_faction = FACTION_DATA[target_faction_id]
                        quest_template_key = random.choice(list(QUEST_TEMPLATES.keys()))
                        quest_template = QUEST_TEMPLATES[quest_template_key]

                        # Create a dummy quest object for the briefing
                        from .quests import Quest
                        quest = Quest(
                            name=quest_template["name"].format(target_faction_name=target_faction["name"]),
                            description=quest_template["description"].format(
                                quest_giver_faction_name=quest_giver_faction["name"],
                                target_faction_name=target_faction["name"]
                            ),
                            objectives=[],
                            rewards=quest_template["rewards"],
                            quest_giver_faction=quest_giver_faction_id,
                            target_faction=target_faction_id
                        )

                        accepted = draw_quest_briefing(stdscr, quest, color_map)
                        if accepted:
                            game_state.current_quest = quest
                            game_state.city_hall_cooldown = 100
                            game_state.car_world_x, game_state.car_world_y = find_safe_exit_spot(world, building)
                            return True # Exit the interaction
                    elif selected_option == 1: # Ask about this town
                        # Get town info
                        faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
                        info = CITY_INFO.get(f"{faction_id}_hub", CITY_INFO["generic_procedural"])
                        draw_dialog_modal(stdscr, [info["description"]], color_map)
                        rendering_queue.draw(stdscr)
                        stdscr.nodelay(0) # Wait for user input
                        stdscr.getch()
                        stdscr.nodelay(1) # Return to non-blocking mode
                    elif selected_option == 2: # Leave
                        game_state.city_hall_cooldown = 100
                        game_state.car_world_x, game_state.car_world_y = find_safe_exit_spot(world, building)
                        return True
            return True # Found a city hall and interacted.
    return False

