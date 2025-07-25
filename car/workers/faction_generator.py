import logging
from typing import Any, Dict

def generate_factions_worker(pipeline: Any) -> Dict:
    """
    A synchronous worker that calls the LLM to generate faction data.
    This is designed to be run in a thread to avoid blocking the UI.
    """
    from ..logic.llm_faction_generator import generate_factions_from_llm
    
    logging.info("Faction generator worker started.")
    try:
        faction_data = generate_factions_from_llm(pipeline)
        logging.info("Faction generator worker finished successfully.")
        return faction_data
    except Exception as e:
        logging.error(f"Faction generator worker failed: {e}", exc_info=True)
        return None
