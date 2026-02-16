import logging
from typing import Dict, Tuple
from .prompt_builder import build_faction_prompt
from .llm_inference import generate_json
from .llm_schemas import FACTION_SCHEMA

def generate_factions_from_llm(app, theme: dict) -> Tuple[Dict, bool]:
    """
    Generates a new set of factions by calling the language model, guided by a theme.
    Returns (factions_dict, is_fallback) where is_fallback=True if LLM generation failed.
    """
    prompt = build_faction_prompt(theme)

    faction_data = generate_json(app, prompt, json_schema=FACTION_SCHEMA, max_tokens=2048, temperature=0.8)

    if faction_data is None:
        logging.warning("Faction generation returned None — using fallback factions.")
        return _get_fallback_factions(), True

    # --- Process the response ---
    if not isinstance(faction_data, dict) or "error" in faction_data:
        details = faction_data.get('details', 'No details') if isinstance(faction_data, dict) else "Non-dict response"
        logging.error(f"Faction generation failed: {details}")
        return _get_fallback_factions(), True

    return faction_data, False

def _get_fallback_factions():
    """Returns a hardcoded fallback response for testing or when the LLM is unavailable."""
    return {
      "the_vultures": {
        "name": "The Vultures", "description": "Vicious scavengers who live by the creed of might makes right.", "hub_city_coordinates": (-30, 30), "control": 50,
        "relationships": {"desert_rats": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Neutral", "the_junction": "Neutral"},
        "units": ["rust_bucket", "raider_buggy", "technical"],
        "unit_names": {
            "rust_bucket": {"name": "Carrion Bomb", "description": "A rusted wreck packed with explosives, aimed at you."},
            "raider_buggy": {"name": "Talon Runner", "description": "Stripped-down buggy built for brutal hit-and-run attacks."},
            "technical": {"name": "Gut Wagon", "description": "Salvaged pickup with a jury-rigged gun mount."},
        },
        "faction_boss": {"name": "Scrap King Klaw", "vehicle": "war_rig", "hp_multiplier": 5.0, "damage_multiplier": 2.5}
      },
      "desert_rats": {
        "name": "Desert Rats", "description": "Nomadic speed demons who value freedom and fast cars above all else.", "hub_city_coordinates": (40, -20), "control": 50,
        "relationships": {"the_vultures": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Allied", "the_junction": "Neutral"},
        "units": ["motorcycle", "hotrod", "muscle_car"],
        "unit_names": {
            "motorcycle": {"name": "Dust Devil", "description": "Lightning-fast bike that strikes before you hear it."},
            "hotrod": {"name": "Sandstorm", "description": "Souped-up hot rod trailing flames across the dunes."},
            "muscle_car": {"name": "Thunder Rat", "description": "Roaring muscle car with a supercharged engine."},
        },
        "faction_boss": {"name": "Road Captain Fury", "vehicle": "sports_car", "hp_multiplier": 3.0, "damage_multiplier": 3.5}
      },
      "corporate_guard": {
        "name": "Corporate Guard", "description": "Remnants of a pre-apocalypse corporation, seeking to restore order through force.", "hub_city_coordinates": (25, 50), "control": 50,
        "relationships": {"the_vultures": "Hostile", "desert_rats": "Hostile", "the_convoy": "Hostile", "the_junction": "Neutral"},
        "units": ["sedan", "armored_truck", "peacekeeper"],
        "unit_names": {
            "sedan": {"name": "Enforcer", "description": "Standard-issue corporate patrol sedan, reliable and armored."},
            "armored_truck": {"name": "Bulwark", "description": "Heavily plated security transport, nearly unstoppable."},
            "peacekeeper": {"name": "Sentinel", "description": "Fast-response vehicle for corporate law enforcement."},
        },
        "faction_boss": {"name": "Commander Valerius", "vehicle": "hatchback", "hp_multiplier": 4.0, "damage_multiplier": 3.0}
      },
      "the_convoy": {
        "name": "The Convoy", "description": "A massive, mobile city of traders and merchants, always on the move.", "hub_city_coordinates": (-40, -35), "control": 50,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Allied", "corporate_guard": "Hostile", "the_junction": "Neutral"},
        "units": ["truck", "van", "panel_wagon"],
        "unit_names": {
            "truck": {"name": "Hauler", "description": "Heavy cargo truck repurposed for convoy defense."},
            "van": {"name": "Tinker Van", "description": "Mobile workshop packed with trade goods and tools."},
            "panel_wagon": {"name": "Peddler", "description": "Armored merchant wagon that doubles as a battering ram."},
        },
        "faction_boss": {"name": "The Quartermaster", "vehicle": "truck", "hp_multiplier": 6.0, "damage_multiplier": 2.0}
      },
      "the_junction": {
        "name": "The Junction", "description": "A neutral oasis of commerce and diplomacy in the heart of the wasteland.", "hub_city_coordinates": (0, 0), "control": 100,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Neutral", "corporate_guard": "Neutral", "the_convoy": "Neutral"},
        "units": ["rusty_sedan", "guard_truck"],
        "unit_names": {
            "rusty_sedan": {"name": "Junction Runner", "description": "Beat-up sedan used for local courier runs."},
            "guard_truck": {"name": "Watchtower", "description": "Armored truck patrolling the neutral zone perimeter."},
        },
        "faction_boss": None
      }
    }
