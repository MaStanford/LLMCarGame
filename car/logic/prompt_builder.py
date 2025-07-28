import json
import os
import logging
from ..logic.data_loader import FACTION_DATA as GLOBAL_FACTION_DATA
from ..logic.entity_loader import ALL_VEHICLES

def _format_player_state(game_state):
    """Formats the player's current status into a string for the LLM."""
    # For workers, game_state might be a SimpleNamespace with no car
    car_name = getattr(getattr(game_state, 'player_car', None), 'name', 'Unknown')
    car_color = getattr(game_state, 'car_color_names', ['Unknown'])[0]
    
    # Handle mounted weapons carefully
    mounted_weapons_dict = getattr(game_state, 'mounted_weapons', {})
    mounted_weapons = [w.name for w in mounted_weapons_dict.values() if w]

    return (
        f"- Level: {getattr(game_state, 'player_level', 1)} ({getattr(game_state, 'current_xp', 0)}/{getattr(game_state, 'xp_to_next_level', 1000)} XP)\n"
        f"- Cash: ${getattr(game_state, 'player_cash', 0)}\n"
        f"- Vehicle: {car_name} ({car_color})\n"
        f"- Durability: {getattr(game_state, 'current_durability', 100)}/{getattr(game_state, 'max_durability', 100)}\n"
        f"- Mounted Weapons: {', '.join(mounted_weapons) if mounted_weapons else 'None'}"
    )

def _format_world_state(faction_data, game_state):
    """Formats the world's faction status into a string for the LLM."""
    report = []
    for faction_id, data in faction_data.items():
        control = game_state.faction_control.get(faction_id, data.get("control", 50))
        
        # Check if 'description' exists, provide a default if not.
        vibe = data.get('description', 'No description available.')
        report.append(f"\n### {data['name']}\n- Vibe: {vibe}\n- Control: {control}% ")

        # Safely build relationships string
        relationships_list = []
        for other_id, status in data.get("relationships", {}).items():
            if other_id in faction_data:
                relationships_list.append(f"{faction_data[other_id]['name']} ({status})")
            else:
                logging.warning(f"Relationship formatting skipped for missing faction ID: {other_id}")
        
        relationships = ", ".join(relationships_list)
        report.append(f"- Relationships: {relationships}")
    return "\n".join(report)

def _format_narrative_history(game_state):
    """Formats the completed quest log into a string for the LLM."""
    quest_log = getattr(game_state, 'quest_log', [])
    
    # In a live game, the quest log might be empty, so we load from file.
    if not quest_log and os.path.exists("temp/quest_log.json"):
        with open("temp/quest_log.json", "r") as f:
            try:
                quest_log = json.load(f)
            except (json.JSONDecodeError, IndexError):
                quest_log = []

    if not quest_log:
        return "Player has not completed any quests yet."

    history = [f"- \"{item['name']}\"" for item in quest_log[-5:]]
    
    return (
        f"Player has completed {len(quest_log)} quests.\n"
        f"Recent history:\n"
        + "\n".join(history)
    )


def _get_vehicle_list():
    """Returns a formatted string of available vehicles for prompts."""
    return ", ".join([vehicle.__name__ for vehicle in ALL_VEHICLES])

def build_quest_prompt(game_state, faction_data_override=None):
    """
    Builds the complete, dynamic prompt for quest generation.
    Uses faction_data_override if provided, otherwise falls back to the global import.
    """
    faction_data = faction_data_override if faction_data_override is not None else GLOBAL_FACTION_DATA
    theme = getattr(game_state, 'theme', {'name': 'Default', 'description': 'A standard wasteland adventure.'})

    with open("prompts/game_context.txt", "r") as f:
        game_summary = f.read()
        
    player_state = _format_player_state(game_state)
    world_state = _format_world_state(faction_data, game_state)
    narrative_history = _format_narrative_history(game_state)
    theme_str = f"The current theme is '{theme['name']}': {theme['description']}"
    
    with open("prompts/quest_prompt.txt", "r") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.replace("{{ game_summary }}", game_summary)
    prompt = prompt.replace("{{ player_state }}", player_state)
    prompt = prompt.replace("{{ world_state }}", world_state)
    prompt = prompt.replace("{{ narrative_history }}", narrative_history)
    prompt = prompt.replace("{{ theme }}", theme_str)
    
    logging.info(f"--- BUILT QUEST PROMPT ---\n{prompt}\n--------------------------")
    return prompt

def build_faction_prompt(theme: dict):
    """Builds the complete, dynamic prompt for faction generation."""
    with open("prompts/game_context.txt", "r") as f:
        game_context = f.read()

    with open("prompts/faction_generation_prompt.txt", "r") as f:
        prompt_template = f.read()
        
    theme_str = f"The chosen theme for this world is '{theme['name']}': {theme['description']}"
    prompt = prompt_template.replace("{{ game_context }}", game_context)
    prompt = prompt.replace("{{ vehicle_list }}", _get_vehicle_list())
    prompt = prompt.replace("{{ theme }}", theme_str)

    logging.info(f"--- BUILT FACTION PROMPT ---\n{prompt}\n--------------------------")
    return prompt
