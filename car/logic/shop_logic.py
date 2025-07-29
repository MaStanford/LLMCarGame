from ..data.weapons import WEAPONS_DATA
from ..entities.weapon import Weapon
from ..world.generation import get_city_faction

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
    Gets the inventory for a given shop type, influenced by faction control.
    """
    inventory = []
    
    # Determine the local faction and their control level
    local_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y, game_state.factions)
    faction_control = game_state.faction_control.get(local_faction_id, 50)
    
    # Price volatility: 0.5 means prices can vary by +/- 50%
    price_volatility = 0.5 
    # Price modifier is inversely proportional to control
    price_modifier = 1 + ((50 - faction_control) / 50) * price_volatility

    # The neutral hub always has stable prices
    if game_state.factions[local_faction_id].get("hub_city_coordinates") == [0, 0]:
        price_modifier = 1.0

    if shop_type == "weapon_shop":
        # If faction control is too low, the shop is empty
        if faction_control < 20:
            return [] 
            
        # For now, sell all base weapons
        for weapon_id in WEAPONS_DATA:
            weapon = Weapon(weapon_id)
            inventory.append({
                "type": "weapon",
                "name": weapon.name,
                "damage": weapon.damage,
                "range": weapon.range,
                "fire_rate": weapon.fire_rate,
                "price": int(weapon.price * price_modifier),
                "item_id": weapon_id,
                "modifiers": weapon.modifiers,
            })
    elif shop_type == "mechanic_shop":
        inventory.append({"type": "repair", "name": "Full Repair", "price": int(100 * price_modifier)})
    elif shop_type == "gas_station":
        inventory.append({"type": "gas", "name": "Fill Tank", "price": int(50 * price_modifier)})
        
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

