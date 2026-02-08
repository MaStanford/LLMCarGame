import logging
import json
from typing import Any, Dict, Optional
from .llm_inference import generate_json
from .llm_schemas import ITEM_SCHEMA
from ..data.cosmetics import COSMETIC_TAGS
from ..data.weapons import WEAPONS_DATA

def validate_generated_item(item_data: Dict, base_item_template: Dict) -> bool:
    """
    Rigorously validates the JSON object returned by the LLM for a generated item.
    """
    if not isinstance(item_data, dict):
        logging.error(f"Validation failed: Generated item is not a dictionary.")
        return False

    required_keys = ["name", "base_item_id", "description", "stat_modifiers", "cosmetic_tags", "rarity"]
    for key in required_keys:
        if key not in item_data:
            logging.error(f"Validation failed: Missing required key '{key}'.")
            return False

    if not isinstance(item_data["name"], str) or not item_data["name"]:
        logging.error(f"Validation failed: 'name' must be a non-empty string.")
        return False

    # Check base_item_id instead of base_item
    if item_data["base_item_id"] != base_item_template["id"]:
        logging.error(f"Validation failed: 'base_item_id' ({item_data['base_item_id']}) does not match template ({base_item_template['id']}).")
        return False

    if not isinstance(item_data["stat_modifiers"], dict):
        logging.error(f"Validation failed: 'stat_modifiers' must be a dictionary.")
        return False

    for stat, value in item_data["stat_modifiers"].items():
        # Relaxed check for stats, as they might vary
        if not isinstance(value, (int, float)) or not (0.5 <= value <= 2.0):
            logging.error(f"Validation failed: Modifier for '{stat}' ({value}) is not a number or is out of the acceptable range (0.5-2.0).")
            return False

    if not isinstance(item_data["cosmetic_tags"], list):
        logging.error(f"Validation failed: 'cosmetic_tags' must be a list.")
        return False

    return True

def generate_item_from_llm(app: Any, theme: Dict, player_level: int, base_item_id: str) -> Optional[Dict]:
    """
    Generates a unique item variant using the LLM.
    Returns the validated JSON data for the new item, or None if generation or validation fails.
    """
    logging.info(f"Attempting to generate a new item based on '{base_item_id}'...")

    base_item_template = WEAPONS_DATA.get(base_item_id)
    if not base_item_template:
        logging.error(f"Could not find base item template for ID: {base_item_id}")
        return None

    # Add the ID to the template for the prompt
    base_item_template["id"] = base_item_id

    try:
        with open("prompts/item_generator_prompt.txt", "r") as f:
            prompt_template = f.read()

        # Build game summary for context
        game_summary = "A post-apocalyptic automotive RPG where players survive and upgrade their vehicles."

        prompt = prompt_template.replace("{{ game_summary }}", game_summary)
        prompt = prompt.replace("{{ theme }}", f"'{theme['name']}': {theme['description']}")
        prompt = prompt.replace("{{ base_item_data }}", json.dumps(base_item_template, indent=2))

        response = generate_json(app, prompt, json_schema=ITEM_SCHEMA, max_tokens=512, temperature=0.8)
        if response and isinstance(response, dict):
            if validate_generated_item(response, base_item_template):
                logging.info(f"Successfully generated and validated new item: {response['name']}")
                return response
            else:
                logging.error("Generated item failed validation.")
                return None

    except Exception as e:
        logging.error(f"An error occurred during item generation: {e}", exc_info=True)

    return None
