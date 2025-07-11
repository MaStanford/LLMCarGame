import random
from ..data.weapons import WEAPONS_DATA
from ..data.game_constants import FUEL_PRICE, REPAIR_PRICE
from .modifier_logic import generate_weapon_modifiers
from ..entities.weapon import Weapon

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
        inventory.append({"name": "Purchase New Attachment Point", "type": "purchase_attachment", "price": 500})
        inventory.append({"name": "Upgrade Attachment Point Size", "type": "upgrade_attachment", "price": 1000})

    elif shop_type == "weapon":
        # Add ammo for different weapon types
        for weapon_id, weapon_data in WEAPONS_DATA.items():
            if player_level >= weapon_data.get("min_level", 1):
                ammo_type = weapon_data["ammo_type"]
                price = int(weapon_data["price"] * price_modifier)
                inventory.append({
                    "name": f"{ammo_type.replace('_', ' ').title()} Ammo",
                    "type": "ammo",
                    "ammo_type": ammo_type,
                    "amount": weapon_data.get("ammo_per_clip", 10),
                    "price": price
                })
        
        # Add weapons with potential modifiers
        for weapon_id, weapon_data in WEAPONS_DATA.items():
            if player_level >= weapon_data.get("min_level", 1):
                luck_factor = 1.0 + (town_reputation / 100.0) # Reputation increases luck
                modifiers = generate_weapon_modifiers(player_level, luck_factor)
                weapon = Weapon(weapon_id, modifiers)
                
                price = int(weapon_data["price"] * price_modifier * (1 + len(modifiers) * 0.5)) # Modifiers increase price
                
                inventory.append({
                    "name": weapon.name,
                    "type": "weapon",
                    "weapon_id": weapon_id,
                    "price": price,
                    "item": weapon
                })

    return inventory
