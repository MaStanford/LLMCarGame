import logging
import json
from typing import Any, Dict
from .gemini_cli import generate_with_gemini_cli

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

    if app.generation_mode == "gemini_cli":
        response = generate_with_gemini_cli(prompt, parse_json=True)
        if isinstance(response, dict) and "error" not in response:
            return response
        else:
            logging.error(f"Failed to generate world details, using fallback. Response: {response}")
            # Fallback to prevent crash
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
    else: # local mode
        logging.info("Local generation mode for world details, returning basic names.")
        # Create a basic mapping from coordinates to faction names for cities
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
