import json
import os
from ..logic.data_loader import FACTION_DATA
from ..logic.entity_loader import ALL_VEHICLES

def _format_player_state(game_state):
    """Formats the player's current status into a string for the LLM."""
    car = game_state.player_car
    mounted_weapons = [w.name for w in game_state.mounted_weapons.values() if w]
    
    return (
        f"- Level: {game_state.player_level} ({game_state.current_xp}/{game_state.xp_to_next_level} XP)\n"
        f"- Cash: ${game_state.player_cash}\n"
        f"- Vehicle: {car.name} ({game_state.car_color_names[0]})\n"
        f"- Durability: {game_state.current_durability}/{game_state.max_durability}\n"
        f"- Mounted Weapons: {', '.join(mounted_weapons) if mounted_weapons else 'None'}"
    )

def _format_world_state():
    """Formats the world's faction status into a string for the LLM."""
    report = []
    for faction_id, data in FACTION_DATA.items():
        report.append(f"\n### {data['name']}\n- Vibe: {data.get('description', 'N/A')}\n- Control: {data['control']}% ")
        relationships = ", ".join([f"{FACTION_DATA[other_id]['name']} ({status})" for other_id, status in data["relationships"].items()])
        report.append(f"- Relationships: {relationships}")
    return "\n".join(report)

def _format_narrative_history():
    """Formats the completed quest log into a string for the LLM."""
    quest_log_path = "temp/quest_log.json"
    if not os.path.exists(quest_log_path):
        return "No significant events have occurred yet."
        
    with open(quest_log_path, "r") as f:
        try:
            log = json.load(f)
            if not log:
                return "No significant events have occurred yet."
            # Format the last 5 quests for brevity
            history = ["- " + item['name'] for item in log[-5:]]
            return "\n".join(history)
        except (json.JSONDecodeError, IndexError):
            return "No significant events have occurred yet."

def _get_vehicle_list():
    """Returns a formatted string of available vehicles for prompts."""
    return ", ".join([vehicle.__name__ for vehicle in ALL_VEHICLES])

def build_quest_prompt(game_state):
    """Builds the complete, dynamic prompt for quest generation."""
    with open("prompts/game_context.txt", "r") as f:
        game_summary = f.read()
        
    player_state = _format_player_state(game_state)
    world_state = _format_world_state()
    narrative_history = _format_narrative_history()
    
    with open("prompts/quest_prompt.txt", "r") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.replace("{{ game_summary }}", game_summary)
    prompt = prompt.replace("{{ player_state }}", player_state)
    prompt = prompt.replace("{{ world_state }}", world_state)
    prompt = prompt.replace("{{ narrative_history }}", narrative_history)
    
    return prompt

def build_faction_prompt():
    """Builds the complete, dynamic prompt for faction generation."""
    with open("prompts/game_context.txt", "r") as f:
        game_context = f.read()

    with open("prompts/faction_generation_prompt.txt", "r") as f:
        prompt_template = f.read()
        
    prompt = prompt_template.replace("{{ game_context }}", game_context)
    prompt = prompt.replace("{{ vehicle_list }}", _get_vehicle_list())

    return prompt
