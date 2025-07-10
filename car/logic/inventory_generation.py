import random
from ..data.weapons import WEAPONS_DATA
from ..data.game_constants import FUEL_PRICE, REPAIR_PRICE

def generate_inventory(shop_type, player_level, town_reputation):
    """
    Generates a dynamic inventory for a shop based on its type, player level, and town reputation.
    """
    inventory = []
    # Apply a price modifier based on town reputation (e.g., -10% to +10%)
    price_modifier = 1.0 - (town_reputation / 500) # Example: rep of 100 = 0.8 modifier

    if shop_type == "gas":
        inventory.append({"name": "Fuel", "type": "fuel", "amount": 25, "price": int(FUEL_PRICE * price_modifier)})
        inventory.append({"name": "Super Fuel", "type": "fuel", "amount": 100, "price": int(FUEL_PRICE * 3.5 * price_modifier)})

    elif shop_type == "mechanic":
        inventory.append({"name": "Tire Patch", "type": "repair", "amount": 25, "price": int(REPAIR_PRICE * price_modifier)})
        inventory.append({"name": "Full Service", "type": "repair", "amount": 100, "price": int(REPAIR_PRICE * 3.5 * price_modifier)})

    elif shop_type == "weapon":
        # Add ammo for different weapon types, potentially filtering by player's weapons
        for weapon_id, weapon in WEAPONS_DATA.items():
            if player_level >= weapon.get("min_level", 1):
                ammo_type = weapon["ammo_type"]
                price = int(weapon["price"] * price_modifier) # Changed from ammo_price
                inventory.append({
                    "name": f"{ammo_type.replace('_', ' ').title()} Ammo",
                    "type": "ammo",
                    "ammo_type": ammo_type,
                    "amount": weapon.get("ammo_per_clip", 10),
                    "price": price
                })
        # Add some weapons to the ammo shop
        for weapon_id, weapon in WEAPONS_DATA.items():
            if player_level >= weapon.get("min_level", 1):
                price = int(weapon["price"] * price_modifier)
                inventory.append({
                    "name": weapon["name"],
                    "type": "weapon",
                    "weapon_id": weapon_id,
                    "price": price,
                    "item": weapon # The actual weapon data
                })

    return inventory
