import logging
from ..data.item_modifiers import RARITY_LEVELS, STAT_MODIFIERS, COSMETIC_TAGS

def validate_generated_item(item_data: dict) -> bool:
    """
    Rigorously checks every key and value in the JSON returned by the LLM.

    Args:
        item_data: The dictionary representing the generated item.

    Returns:
        True if the item data is valid, False otherwise.
    """
    required_keys = ["name", "base_item_id", "description", "rarity", "stat_modifiers", "cosmetic_tags"]
    for key in required_keys:
        if key not in item_data:
            logging.error(f"Generated item missing required key: {key}")
            return False

    if not isinstance(item_data["name"], str) or not item_data["name"]:
        logging.error("Generated item 'name' must be a non-empty string.")
        return False

    if not isinstance(item_data["base_item_id"], str) or not item_data["base_item_id"]:
        logging.error("Generated item 'base_item_id' must be a non-empty string.")
        return False

    if not isinstance(item_data["description"], str):
        logging.error("Generated item 'description' must be a string.")
        return False

    if item_data["rarity"] not in RARITY_LEVELS:
        logging.error(f"Generated item 'rarity' is not a valid rarity level: {item_data['rarity']}")
        return False

    if not isinstance(item_data["stat_modifiers"], dict):
        logging.error("Generated item 'stat_modifiers' must be a dictionary.")
        return False

    for stat, value in item_data["stat_modifiers"].items():
        if stat not in STAT_MODIFIERS:
            logging.error(f"Generated item has an invalid stat modifier: {stat}")
            return False
        min_val, max_val = STAT_MODIFIERS[stat]
        if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
            logging.error(f"Generated item stat '{stat}' has an invalid value: {value}")
            return False

    if not isinstance(item_data["cosmetic_tags"], list):
        logging.error("Generated item 'cosmetic_tags' must be a list.")
        return False

    for tag in item_data["cosmetic_tags"]:
        if tag not in COSMETIC_TAGS:
            logging.error(f"Generated item has an invalid cosmetic tag: {tag}")
            return False

    return True
