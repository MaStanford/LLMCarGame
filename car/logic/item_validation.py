import logging
from ..data.cosmetics import COSMETIC_TAGS
from ..data.weapons import WEAPONS_DATA
from ..logic.entity_loader import get_vehicle_class_by_name

def validate_generated_item(item_data, item_type):
    """
    Rigorously validates the JSON data for a generated item.
    Returns True if valid, False otherwise.
    """
    if not isinstance(item_data, dict):
        logging.error(f"Validation failed: item_data is not a dictionary.")
        return False

    # --- Check for required keys ---
    required_keys = ["name", "base_item", "description", "stat_modifiers", "cosmetic_tags"]
    for key in required_keys:
        if key not in item_data:
            logging.error(f"Validation failed: Missing required key '{key}'.")
            return False

    # --- Validate data types ---
    if not isinstance(item_data["name"], str) or not item_data["name"]:
        logging.error(f"Validation failed: 'name' must be a non-empty string.")
        return False
    if not isinstance(item_data["base_item"], str):
        logging.error(f"Validation failed: 'base_item' must be a string.")
        return False
    if not isinstance(item_data["description"], str):
        logging.error(f"Validation failed: 'description' must be a string.")
        return False
    if not isinstance(item_data["stat_modifiers"], dict):
        logging.error(f"Validation failed: 'stat_modifiers' must be a dictionary.")
        return False
    if not isinstance(item_data["cosmetic_tags"], list):
        logging.error(f"Validation failed: 'cosmetic_tags' must be a list.")
        return False

    # --- Validate base_item existence ---
    if item_type == "weapon":
        if item_data["base_item"] not in WEAPONS_DATA:
            logging.error(f"Validation failed: base_item '{item_data['base_item']}' not found in WEAPONS_DATA.")
            return False
    elif item_type == "vehicle":
        if get_vehicle_class_by_name(item_data["base_item"]) is None:
            logging.error(f"Validation failed: base_item '{item_data['base_item']}' is not a valid vehicle class.")
            return False

    # --- Validate stat_modifiers ---
    for key, value in item_data["stat_modifiers"].items():
        if not isinstance(value, (int, float)):
            logging.error(f"Validation failed: stat_modifier '{key}' has non-numeric value '{value}'.")
            return False
        if not 0.5 <= value <= 1.5:
            logging.error(f"Validation failed: stat_modifier '{key}' value '{value}' is out of range (0.5-1.5).")
            return False

    # --- Validate cosmetic_tags ---
    for tag in item_data["cosmetic_tags"]:
        if tag not in COSMETIC_TAGS:
            logging.warning(f"Validation warning: cosmetic_tag '{tag}' is not in the predefined list.")
            # This is a warning, not a failure, to allow for creative LLM outputs.

    logging.info(f"Successfully validated generated item: {item_data['name']}")
    return True
