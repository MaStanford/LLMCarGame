import logging
from .llm_inference import generate_text

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

    response = generate_text(app, prompt, max_tokens=256, temperature=0.8)
    if response is None:
        return _get_fallback_dialog(player_reputation)
    return response

def _get_fallback_dialog(reputation: int) -> str:
    """Returns a hardcoded fallback dialog based on reputation."""
    if reputation > 50:
        return "Welcome back, friend. Lookin' to upgrade."
    elif reputation < -50:
        return "You got a lot of nerve showin' your face around here. Make it quick."
    else:
        return "What do you need."
