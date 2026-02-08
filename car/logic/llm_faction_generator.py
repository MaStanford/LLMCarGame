import logging
from .prompt_builder import build_faction_prompt
from .llm_inference import generate_json
from .llm_schemas import FACTION_SCHEMA

def generate_factions_from_llm(app, theme: dict):
    """
    Generates a new set of factions by calling the language model, guided by a theme.
    """
    prompt = build_faction_prompt(theme)

    faction_data = generate_json(app, prompt, json_schema=FACTION_SCHEMA, max_tokens=2048, temperature=0.8)

    if faction_data is None:
        return _get_fallback_factions()

    # --- Process the response ---
    if not isinstance(faction_data, dict) or "error" in faction_data:
        details = faction_data.get('details', 'No details') if isinstance(faction_data, dict) else "Non-dict response"
        logging.error(f"Faction generation failed: {details}")
        return _get_fallback_factions()

    return faction_data

def _get_fallback_factions():
    """Returns a hardcoded fallback response for testing or when the LLM is unavailable."""
    return {
      "the_vultures": {
        "name": "The Vultures", "description": "Vicious scavengers who live by the creed of might makes right.", "hub_city_coordinates": [-30, 30], "control": 50,
        "relationships": {"desert_rats": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Neutral", "the_junction": "Neutral"},
        "units": ["rust_bucket", "raider_buggy", "technical"],
        "faction_boss": {"name": "Scrap King Klaw", "vehicle": "war_rig", "hp_multiplier": 5.0, "damage_multiplier": 2.5}
      },
      "desert_rats": {
        "name": "Desert Rats", "description": "Nomadic speed demons who value freedom and fast cars above all else.", "hub_city_coordinates": [40, -20], "control": 50,
        "relationships": {"the_vultures": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Allied", "the_junction": "Neutral"},
        "units": ["motorcycle", "hotrod", "muscle_car"],
        "faction_boss": {"name": "Road Captain Fury", "vehicle": "sports_car", "hp_multiplier": 3.0, "damage_multiplier": 3.5}
      },
      "corporate_guard": {
        "name": "Corporate Guard", "description": "Remnants of a pre-apocalypse corporation, seeking to restore order through force.", "hub_city_coordinates": [25, 50], "control": 50,
        "relationships": {"the_vultures": "Hostile", "desert_rats": "Hostile", "the_convoy": "Hostile", "the_junction": "Neutral"},
        "units": ["sedan", "armored_truck", "peacekeeper"],
        "faction_boss": {"name": "Commander Valerius", "vehicle": "hatchback", "hp_multiplier": 4.0, "damage_multiplier": 3.0}
      },
      "the_convoy": {
        "name": "The Convoy", "description": "A massive, mobile city of traders and merchants, always on the move.", "hub_city_coordinates": [-40, -35], "control": 50,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Allied", "corporate_guard": "Hostile", "the_junction": "Neutral"},
        "units": ["truck", "van", "panel_wagon"],
        "faction_boss": {"name": "The Quartermaster", "vehicle": "truck", "hp_multiplier": 6.0, "damage_multiplier": 2.0}
      },
      "the_junction": {
        "name": "The Junction", "description": "A neutral oasis of commerce and diplomacy in the heart of the wasteland.", "hub_city_coordinates": [0, 0], "control": 100,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Neutral", "corporate_guard": "Neutral", "the_convoy": "Neutral"},
        "units": ["rusty_sedan", "guard_truck"],
        "faction_boss": None
      }
    }
