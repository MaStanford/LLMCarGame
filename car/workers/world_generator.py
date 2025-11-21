import logging
import time
import json
from types import SimpleNamespace
from typing import Any, Dict
from textual.message import Message

from ..logic.llm_faction_generator import generate_factions_from_llm, _get_fallback_factions
from ..logic.llm_quest_generator import generate_quest_from_llm, _get_fallback_quest
from ..logic.llm_world_details_generator import generate_world_details_from_llm
from ..logic.prompt_builder import _format_world_state
from ..logic.gemini_cli import generate_with_gemini_cli

class StageUpdate(Message):
    """A message to update the world building stage."""
    def __init__(self, data: tuple):
        self.data = data
        super().__init__()

def _generate_story_intro(app, theme, factions, neutral_faction_name):
    """Generates the introductory story text."""
    logging.info("Generating story intro...")
    mock_game_state = SimpleNamespace(faction_control={})
    world_state = _format_world_state(factions, mock_game_state)
    
    with open("prompts/story_intro_prompt.txt", "r") as f:
        prompt = f.read()
    
    prompt = prompt.replace("{{ theme }}", f"'{theme['name']}': {theme['description']}")
    prompt = prompt.replace("{{ world_state }}", world_state)
    prompt = prompt.replace("{{ neutral_city_name }}", neutral_faction_name)

    if app.generation_mode == "gemini_cli":
        response = generate_with_gemini_cli(prompt, parse_json=False)
        return response if isinstance(response, str) else "Welcome to the wasteland."
    else:
        return "You arrive at the neutral city of The Junction, a beacon of tense neutrality in a world torn apart by warring factions. Your goal is simple: find the Genesis Module and escape. The road will be long and dangerous. Good luck."


def generate_initial_world_worker(app: Any, new_game_settings: dict) -> Dict:
    """
    A worker that generates the complete initial state for a new world.
    """
    logging.info("Initial world generation worker started.")
    start_time = time.time()
    
    try:
        theme = new_game_settings["theme"]
        logging.info(f"Generating world with theme: {theme['name']}")

        # Stage 1: Generate Factions
        app.post_message(StageUpdate(("stage", "Stage 1: Forging Factions...")))
        time.sleep(0.25)
        if app.generation_mode == "local":
            logging.info("Using local generation mode. Returning fallback factions.")
            factions = _get_fallback_factions()
        else:
            factions = generate_factions_from_llm(app, theme)
        
        if not factions or "error" in factions:
            raise ValueError(f"Faction generation failed: {factions.get('details', 'No details')}")

        neutral_faction_id = next((fid for fid, data in factions.items() if data.get("hub_city_coordinates") == [0, 0]), None)
        if not neutral_faction_id:
            raise ValueError("Could not find a neutral faction at (0,0) in the generated data.")
        neutral_faction_name = factions[neutral_faction_id]['name']

        # Stage 2: Generate World Details
        app.post_message(StageUpdate(("stage", "Naming the dust bowls...")))
        time.sleep(0.25)
        world_details = generate_world_details_from_llm(app, theme, factions)


        # Stage 3: Generate Initial Quests
        app.post_message(StageUpdate(("stage", f"Populating the {theme['name']}...")))
        time.sleep(0.25)
        initial_quests = []
        mock_game_state = SimpleNamespace(
            faction_reputation={}, faction_control={}, quest_log=[],
            difficulty_mods=new_game_settings["difficulty_mods"], theme=theme,
            story_intro="The story is just beginning..."
        )
        for i in range(3):
            if app.generation_mode == "local":
                quest = _get_fallback_quest(neutral_faction_id)
            else:
                quest = generate_quest_from_llm(
                    game_state=mock_game_state, quest_giver_faction_id=neutral_faction_id,
                    app=app, faction_data=factions
                )
            if quest:
                initial_quests.append(quest)

        # Stage 4: Generate Story Intro
        app.post_message(StageUpdate(("stage", "A poet is writing how it begins...")))
        time.sleep(0.25)
        story_intro = _generate_story_intro(app, theme, factions, neutral_faction_name)

        end_time = time.time()
        logging.info(f"Initial world generation finished successfully in {end_time - start_time:.2f} seconds.")
        
        return {
            "factions": factions,
            "quests": initial_quests,
            "neutral_city_id": neutral_faction_id,
            "story_intro": story_intro,
            "world_details": world_details
        }

    except Exception as e:
        end_time = time.time()
        logging.error(f"Initial world generation worker failed after {end_time - start_time:.2f} seconds: {e}", exc_info=True)
        return None
