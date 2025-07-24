from ..data.weapons import WEAPONS_DATA
from ..entities.weapon import Weapon

def purchase_item(game_state, item):
    """Handles the logic for purchasing an item."""
    item_type = item.get("type")
    if item_type == "weapon":
        weapon = Weapon(item["item_id"])
        game_state.player_inventory.append(weapon)
    elif item_type == "repair":
        game_state.current_durability = game_state.max_durability
    elif item_type == "gas":
        game_state.current_gas = game_state.gas_capacity

def get_shop_inventory(shop_type, game_state):
    """
    Gets the inventory for a given shop type.
    (This is a placeholder - will be expanded later)
    """
    inventory = []
    if shop_type == "weapon_shop":
        # For now, sell all base weapons
        for weapon_id in WEAPONS_DATA:
            weapon = Weapon(weapon_id)
            inventory.append({
                "type": "weapon",
                "name": weapon.name,
                "damage": weapon.damage,
                "range": weapon.range,
                "fire_rate": weapon.fire_rate,
                "price": weapon.price,
                "item_id": weapon_id,
                "modifiers": weapon.modifiers,
            })
    elif shop_type == "mechanic_shop":
        inventory.append({"type": "repair", "name": "Full Repair", "price": 100})
    elif shop_type == "gas_station":
        inventory.append({"type": "gas", "name": "Fill Tank", "price": 50})
        
    return inventory

def calculate_sell_price(item, game_state):
    """Calculates the sell price of an item based on various factors."""
    base_price = getattr(item, 'price', 0)
    
    # Placeholder for reputation and level modifiers
    reputation_modifier = 1.0 # Neutral
    level_modifier = 1.0 + (game_state.player_level * 0.05) # 5% bonus per level
    
    # Sell price is a fraction of the base price
    sell_price = int(base_price * 0.5 * reputation_modifier * level_modifier)
    
    return sell_price
