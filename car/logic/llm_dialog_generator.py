import logging
from ..logic.prompt_builder import build_quest_prompt # Re-using to get context
from ..logic.gemini_cli import generate_with_gemini_cli
from ..logic.llm_faction_generator import _get_fallback_factions

def generate_shop_dialog_from_llm(app, theme: dict, shop_type: str, faction_name: str, faction_vibe: str, player_reputation: int) -> str:
    """
    Generates a short, thematic greeting from a shopkeeper.
    """
    with open("prompts/shop_dialog_prompt.txt", "r") as f:
        prompt = f.read()

    prompt = prompt.replace("{{ theme }}", f"'{theme['name']}': {theme['description']}")
    prompt = prompt.replace("{{ shop_type }}", shop_type)
    prompt = prompt.replace("{{ faction_name }}", faction_name)
    prompt = prompt.replace("{{ faction_vibe }}", faction_vibe)
    prompt = prompt.replace("{{ player_reputation }}", str(player_reputation))

    logging.info(f"--- BUILDING SHOP DIALOG PROMPT ---\n{prompt}\n---------------------------------")

    if app.generation_mode == "gemini_cli":
        response = generate_with_gemini_cli(prompt)
        # The CLI often returns just the string, which is what we want.
        # If it returns a dict with an error, we'll fall back.
        if isinstance(response, dict) and "error" in response:
            logging.error(f"Gemini CLI failed for dialog: {response.get('details')}")
            return _get_fallback_dialog(player_reputation)
        return response if isinstance(response, str) else str(response)

    else:
        # Local LLM is not reliable for creative text, return a fallback.
        logging.info("Local mode active for dialog, returning fallback.")
        return _get_fallback_dialog(player_reputation)

def _get_fallback_dialog(reputation: int) -> str:
    """Returns a hardcoded fallback dialog based on reputation."""
    if reputation > 50:
        return "Welcome back, friend. Lookin' to upgrade."
    elif reputation < -50:
        return "You got a lot of nerve showin' your face around here. Make it quick."
    else:
        return "What do you need."
