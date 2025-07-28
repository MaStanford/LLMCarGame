import logging
from typing import Any, Dict

from ..logic.llm_dialog_generator import generate_shop_dialog_from_llm

def generate_dialog_worker(app: Any, theme: dict, shop_type: str, faction_name: str, faction_vibe: str, player_reputation: int) -> str:
    """
    A worker that generates a short dialog string for a shopkeeper.
    """
    logging.info(f"Dialog worker started for {shop_type} in {faction_name}.")
    
    try:
        dialog = generate_shop_dialog_from_llm(
            app,
            theme,
            shop_type,
            faction_name,
            faction_vibe,
            player_reputation
        )
        return dialog
    except Exception as e:
        logging.error(f"Dialog worker failed: {e}", exc_info=True)
        return "..." # Return a simple fallback on unexpected error
