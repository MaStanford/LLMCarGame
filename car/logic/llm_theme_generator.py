import logging
from typing import List, Dict
from .llm_inference import generate_json
from .llm_schemas import THEME_SCHEMA

def generate_themes_from_llm(app) -> List[Dict[str, str]]:
    """
    Generates a list of three distinct themes for the game, using either the local
    LLM pipeline or the Gemini CLI based on the current settings.
    """
    with open("prompts/theme_generation_prompt.txt", "r") as f:
        prompt = f.read()

    logging.info(f"--- BUILDING THEME PROMPT ---\n{prompt}\n---------------------------")

    theme_data = generate_json(app, prompt, json_schema=THEME_SCHEMA, max_tokens=512, temperature=0.9)

    if theme_data is None:
        return _get_fallback_themes()

    # --- Process the response ---
    if not isinstance(theme_data, dict) or "error" in theme_data:
        details = theme_data.get('details', 'No details') if isinstance(theme_data, dict) else "Non-dict response"
        logging.error(f"Theme generation failed: {details}")
        return _get_fallback_themes()

    if "themes" in theme_data and isinstance(theme_data["themes"], list) and len(theme_data["themes"]) == 3:
        return theme_data["themes"]
    else:
        logging.error(f"LLM output for themes has incorrect structure: {theme_data}")
        return _get_fallback_themes()

def _get_fallback_themes() -> List[Dict[str, str]]:
    """Returns a hardcoded list of themes for testing or when the LLM is unavailable."""
    return [
        {
            "name": "Classic Wasteland",
            "description": "A sun-scorched desert world of rust, dust, and desperate battles for the last drops of gasoline."
        },
        {
            "name": "Cyberpunk Drifters",
            "description": "Neon-drenched cityscapes at night, where cybernetically enhanced drivers clash in high-tech, corporate-sponsored duels."
        },
        {
            "name": "Mutant Menace",
            "description": "A world twisted by radiation, where bizarre creatures roam and strange new powers are waiting to be discovered."
        }
    ]
