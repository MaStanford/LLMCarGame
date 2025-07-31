import logging
from typing import Any, Dict, List

from ..logic.llm_quest_generator import generate_quest_from_llm

def generate_quests_worker(app: Any, city_id: str, city_faction_id: str, theme: dict, faction_data: Dict, story_intro: str) -> List:
    """
    A worker that generates a set of quests for a specific city.
    """
    from types import SimpleNamespace

    logging.info(f"Quest generator worker started for city {city_id} (Faction: {city_faction_id}).")
    
    # Create a mock game_state with the necessary info for the prompt builder
    mock_game_state = SimpleNamespace(
        faction_reputation={},
        faction_control={},
        quest_log=[],
        theme=theme,
        story_intro=story_intro,
        # The prompt builder doesn't need difficulty mods for quest gen
        difficulty_mods={}, 
    )

    generated_quests = []
    for i in range(3):
        logging.info(f"Generating quest {i+1} for {city_id}...")
        quest = generate_quest_from_llm(
            game_state=mock_game_state,
            quest_giver_faction_id=city_faction_id,
            app=app,
            faction_data=faction_data
        )
        if quest:
            generated_quests.append(quest)

    logging.info(f"Quest generator worker for {city_id} finished with {len(generated_quests)} quests.")
    logging.info(f"Generated quests: {generated_quests}")
    return generated_quests