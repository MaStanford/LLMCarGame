import logging
import json
from typing import Any, Dict
from .llm_inference import generate_json
from .llm_schemas import WORLD_DETAILS_SCHEMA

def generate_world_details_from_llm(app: Any, theme: Dict, factions: Dict) -> Dict:
    """
    Generates world details (city names, landmarks, etc.) using the LLM.
    """
    logging.info("Generating world details from LLM...")

    with open("prompts/world_details_prompt.txt", "r") as f:
        prompt = f.read()

    # The prompt uses {{ theme }} and {{ factions }} placeholders
    prompt = prompt.replace("{{ theme }}", f"'{theme['name']}': {theme['description']}")
    prompt = prompt.replace("{{ factions }}", json.dumps(factions, indent=2))

    response = generate_json(app, prompt, json_schema=WORLD_DETAILS_SCHEMA, max_tokens=1024, temperature=0.7)

    if response is not None:
        return response

    # Fallback: build basic city names from faction data
    logging.warning("World details generation failed, using fallback.")
    cities = {}
    for faction_id, faction_data in factions.items():
        if "hub_city_coordinates" in faction_data:
            coords = tuple(faction_data["hub_city_coordinates"])
            cities[f"{coords[0]},{coords[1]}"] = f"The City of {faction_data['name']}"
    return {
        "cities": cities,
        "roads": [],
        "landmarks": []
    }
