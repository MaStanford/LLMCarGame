import logging
import time
from typing import Any, Dict

def generate_factions_worker(pipeline: Any) -> Dict:
    """
    A synchronous worker that calls the LLM to generate faction data.
    This is designed to be run in a thread to avoid blocking the UI.
    """
    from ..logic.llm_faction_generator import generate_factions_from_llm
    
    logging.info("Faction generator worker started.")
    start_time = time.time()
    try:
        faction_data = generate_factions_from_llm(pipeline)
        end_time = time.time()
        logging.info(f"Faction generator worker finished successfully in {end_time - start_time:.2f} seconds.")
        return faction_data
    except Exception as e:
        end_time = time.time()
        logging.error(f"Faction generator worker failed after {end_time - start_time:.2f} seconds: {e}", exc_info=True)
        return None
