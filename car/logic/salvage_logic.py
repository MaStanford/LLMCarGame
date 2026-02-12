RARITY_SCRAP_MULTIPLIERS = {
    "common": 1,
    "uncommon": 2,
    "rare": 4,
    "epic": 8,
    "legendary": 16,
}


def calculate_scrap_value(item):
    """Calculate scrap value for any item (Weapon or Equipment)."""
    base_price = getattr(item, 'price', 0)
    rarity = getattr(item, 'rarity', 'common')
    base_scrap = max(1, int(base_price * 0.10))
    multiplier = RARITY_SCRAP_MULTIPLIERS.get(rarity, 1)
    return base_scrap * multiplier


def salvage_item(game_state, item):
    """Removes item from inventory and grants scrap. Returns scrap amount."""
    scrap = calculate_scrap_value(item)
    game_state.player_scrap += scrap
    game_state.player_inventory.remove(item)
    return scrap
