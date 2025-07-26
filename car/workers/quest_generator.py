import logging
from typing import Any, Dict, List

def generate_quests_worker(pipeline: Any, game_state: Any, city_id: str, num_quests: int) -> List:
    """
    A synchronous worker that calls the LLM to generate a batch of quests.
    """
    from ..logic.llm_quest_generator import generate_quest_from_llm
    
    logging.info(f"Quest generator worker started for city {city_id}.")
    try:
        quests = [generate_quest_from_llm(game_state, city_id, pipeline) for _ in range(num_quests)]
        logging.info(f"Quest generator worker for {city_id} finished successfully.")
        return quests
    except Exception as e:
        logging.error(f"Quest generator worker for {city_id} failed: {e}", exc_info=True)
        return []
