import logging
import time
from types import SimpleNamespace
from typing import Any, Dict

from ..logic.llm_faction_generator import generate_factions_from_llm, _get_fallback_factions
from ..logic.llm_quest_generator import generate_quest_from_llm, _get_fallback_quest

def generate_initial_world_worker(app: Any, new_game_settings: dict) -> Dict:
    """
    A worker that generates the complete initial state for a new world,
    including factions and the first set of quests, based on a chosen theme.
    """
    logging.info("Initial world generation worker started.")
    start_time = time.time()
    
    try:
        theme = new_game_settings["theme"]
        logging.info(f"Generating world with theme: {theme['name']}")

        # 1. Generate Factions
        if app.generation_mode == "local":
            logging.info("Using local generation mode. Returning fallback factions.")
            factions = _get_fallback_factions()
        else:
            factions = generate_factions_from_llm(app, theme)
        
        if not factions or "error" in factions:
            raise ValueError(f"Faction generation failed: {factions.get('details', 'No details')}")

        # 2. Find the Neutral Faction
        neutral_faction_id = None
        for faction_id, data in factions.items():
            if data.get("hub_city_coordinates") == [0, 0]:
                neutral_faction_id = faction_id
                break
        
        if not neutral_faction_id:
            raise ValueError("Could not find a neutral faction at (0,0) in the generated data.")

        logging.info(f"Neutral faction identified: {neutral_faction_id}")

        # 3. Generate Initial Quests for the Neutral Hub
        initial_quests = []
        mock_game_state = SimpleNamespace(
            faction_reputation={},
            faction_control={},
            quest_log=[],
            difficulty_mods=new_game_settings["difficulty_mods"],
            theme=theme
        )

        logging.info("Generating initial quests for the neutral hub...")
        for i in range(3):
            logging.info(f"Generating quest {i+1}...")
            if app.generation_mode == "local":
                quest = _get_fallback_quest(neutral_faction_id)
            else:
                quest = generate_quest_from_llm(
                    game_state=mock_game_state,
                    quest_giver_faction_id=neutral_faction_id,
                    app=app,
                    faction_data=factions
                )
            if quest:
                initial_quests.append(quest)
        
        if len(initial_quests) < 3:
            logging.warning("Failed to generate all initial quests. The game will proceed with fewer quests.")

        end_time = time.time()
        logging.info(f"Initial world generation finished successfully in {end_time - start_time:.2f} seconds.")
        
        return {
            "factions": factions,
            "quests": initial_quests,
            "neutral_city_id": neutral_faction_id
        }

    except Exception as e:
        end_time = time.time()
        logging.error(f"Initial world generation worker failed after {end_time - start_time:.2f} seconds: {e}", exc_info=True)
        return None
