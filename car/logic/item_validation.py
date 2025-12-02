# car/logic/item_validation.py

from car.data.item_modifiers import STAT_MODIFIERS, COSMETIC_TAGS, RARITY_LEVELS

def validate_generated_item(item_data: dict) -> bool:
    """
    Validates a generated item against the defined data structures.

    Args:
        item_data: A dictionary representing the generated item.

    Returns:
        True if the item is valid, False otherwise.
    """
    # Validate top-level keys
    required_keys = ["name", "base_item_id", "description", "rarity", "stat_modifiers", "cosmetic_tags"]
    if not all(key in item_data for key in required_keys):
        # logging.error(f"Missing required key in item data: {item_data}")
        return False

    # Validate data types
    if not isinstance(item_data["name"], str) or not item_data["name"]:
        return False
    if not isinstance(item_data["base_item_id"], str) or not item_data["base_item_id"]:
        return False
    if not isinstance(item_data["description"], str) or not item_data["description"]:
        return False
    if not isinstance(item_data["rarity"], str):
        return False
    if not isinstance(item_data["stat_modifiers"], dict):
        return False
    if not isinstance(item_data["cosmetic_tags"], list):
        return False

    # Validate rarity
    if item_data["rarity"] not in RARITY_LEVELS:
        return False

    # Validate stat modifiers
    for stat, value in item_data["stat_modifiers"].items():
        if stat not in STAT_MODIFIERS:
            return False
        if not isinstance(value, (int, float)):
            return False
        min_mod, max_mod = STAT_MODIFIERS[stat]
        if not (min_mod <= value <= max_mod):
            return False

    # Validate cosmetic tags
    for tag in item_data["cosmetic_tags"]:
        if not isinstance(tag, str):
            return False
        if tag not in COSMETIC_TAGS:
            return False

    return True