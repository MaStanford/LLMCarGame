import curses
from ..ui.city_hall import draw_city_hall_menu, draw_town_info_dialog, draw_quest_briefing
from ..data.city_info import CITY_INFO
from .quests import QUEST_TEMPLATES
from ..data.factions import FACTION_DATA
from ..world.generation import get_city_faction
import random

def handle_city_hall_interaction(stdscr, game_state):
    """
    Handles the player's interaction with a City Hall, including viewing quests and town info.
    """
    selected_option = 0
    menu_options = ["View Contracts", "Ask about this town", "Leave"]

    while True:
        draw_city_hall_menu(stdscr, menu_options, selected_option, game_state.color_map)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_option = (selected_option - 1) % len(menu_options)
        elif key == curses.KEY_DOWN:
            selected_option = (selected_option + 1) % len(menu_options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if selected_option == 0: # View Contracts
                # Generate a quest
                quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
                quest_giver_faction = FACTION_DATA[quest_giver_faction_id]
                hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
                if not hostile_factions:
                    draw_town_info_dialog(stdscr, "No available contracts at this time.", game_state.color_map)
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

                accepted = draw_quest_briefing(stdscr, quest, game_state.color_map)
                if accepted:
                    game_state.current_quest = quest
                    return # Exit the interaction
            elif selected_option == 1: # Ask about this town
                # Get town info
                faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
                info = CITY_INFO.get(f"{faction_id}_hub", CITY_INFO["generic_procedural"])
                draw_town_info_dialog(stdscr, info["description"], game_state.color_map)
                stdscr.getch()
            elif selected_option == 2: # Leave
                return
