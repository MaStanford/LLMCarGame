import logging
from .llm_inference import generate_text

def generate_shop_dialog_from_llm(app, theme: dict, shop_type: str, faction_name: str, faction_vibe: str, player_reputation: int) -> dict:
    """
    Generates a short, thematic greeting and a 'can't afford' quip from a shopkeeper.
    Returns a dict with 'greeting' and 'no_cash' keys.
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
    return _parse_dialog_response(response, player_reputation)

def _parse_dialog_response(response: str, reputation: int) -> dict:
    """Parse the LLM response into greeting and no_cash parts."""
    parts = response.split("---")
    greeting = parts[0].strip()
    if len(parts) >= 2:
        no_cash = parts[1].strip()
    else:
        # LLM didn't follow the format — use the whole response as greeting
        no_cash = _get_fallback_dialog(reputation)["no_cash"]
    return {"greeting": greeting, "no_cash": no_cash}

def _get_fallback_dialog(reputation: int) -> dict:
    """Returns hardcoded fallback dialog based on reputation."""
    if reputation > 50:
        return {
            "greeting": "Welcome back, friend. Lookin' to upgrade.",
            "no_cash": "You're a little short, friend. Come back when your pockets are heavier.",
        }
    elif reputation < -50:
        return {
            "greeting": "You got a lot of nerve showin' your face around here. Make it quick.",
            "no_cash": "You can't even afford that? Get out of my shop.",
        }
    else:
        return {
            "greeting": "What do you need.",
            "no_cash": "No cash, no deal. That's how it works out here.",
        }
