from ..data.weapons import WEAPONS_DATA
from ..data.equipment import EQUIPMENT_DATA
from ..data.pickups import (
    AMMO_BULLET, AMMO_HEAVY_BULLET, AMMO_SHOTGUN, AMMO_MINES, AMMO_FUEL,
)
from ..entities.weapon import Weapon
from ..entities.equipment import Equipment
from ..world.generation import get_city_faction

# Ammo shop listings: (display_name, ammo_type, amount, base_price)
AMMO_SHOP_ITEMS = [
    ("Bullets", AMMO_BULLET, 100, 25),
    ("Heavy Rounds", AMMO_HEAVY_BULLET, 50, 50),
    ("Shotgun Shells", AMMO_SHOTGUN, 30, 40),
    ("Mines", AMMO_MINES, 10, 75),
    ("Flamethrower Fuel", AMMO_FUEL, 200, 40),
]

def purchase_item(game_state, item):
    """Handles the logic for purchasing an item."""
    item_type = item.get("type")
    if item_type == "weapon":
        weapon = Weapon(item["item_id"])
        game_state.player_inventory.append(weapon)
    elif item_type == "equipment":
        equipment = Equipment(item["item_id"])
        game_state.player_inventory.append(equipment)
    elif item_type == "repair":
        game_state.current_durability = game_state.max_durability
    elif item_type == "gas":
        game_state.current_gas = game_state.gas_capacity
    elif item_type == "ammo":
        ammo_type = item["ammo_type"]
        amount = item["amount"]
        if ammo_type not in game_state.ammo_counts:
            game_state.ammo_counts[ammo_type] = 0
        game_state.ammo_counts[ammo_type] += amount

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

        # Sell all base weapons
        for weapon_id in WEAPONS_DATA:
            weapon = Weapon(weapon_id)
            inventory.append({
                "type": "weapon",
                "name": weapon.name,
                "damage": weapon.damage,
                "range": weapon.range,
                "fire_rate": weapon.fire_rate,
                "ammo_type": weapon.ammo_type,
                "price": int(weapon.price * price_modifier),
                "item_id": weapon_id,
                "modifiers": weapon.modifiers,
                "rarity": "common",
            })

        # Sell weapon-affinity equipment
        for equip_id, equip_data in EQUIPMENT_DATA.items():
            if equip_data.get("shop_affinity") == "weapon":
                inventory.append({
                    "type": "equipment",
                    "name": equip_data["name"],
                    "slot": equip_data["slot"],
                    "description": equip_data.get("description", ""),
                    "bonuses": equip_data.get("bonuses", {}),
                    "price": int(equip_data["price"] * price_modifier),
                    "item_id": equip_id,
                    "modifiers": {},
                    "rarity": "common",
                })

        # Sell ammo
        for display_name, ammo_type, amount, base_price in AMMO_SHOP_ITEMS:
            inventory.append({
                "type": "ammo",
                "name": f"{display_name} (x{amount})",
                "ammo_type": ammo_type,
                "amount": amount,
                "price": int(base_price * price_modifier),
            })

    elif shop_type == "mechanic_shop":
        # Repair option (only if not already at full durability)
        if game_state.current_durability < game_state.max_durability:
            inventory.append({"type": "repair", "name": "Full Repair", "price": int(100 * price_modifier)})

        # Sell mechanic-affinity equipment
        for equip_id, equip_data in EQUIPMENT_DATA.items():
            if equip_data.get("shop_affinity") == "mechanic":
                inventory.append({
                    "type": "equipment",
                    "name": equip_data["name"],
                    "slot": equip_data["slot"],
                    "description": equip_data.get("description", ""),
                    "bonuses": equip_data.get("bonuses", {}),
                    "price": int(equip_data["price"] * price_modifier),
                    "item_id": equip_id,
                    "modifiers": {},
                    "rarity": "common",
                })

    elif shop_type == "gas_station":
        # Fill Tank option (only if not already at full gas)
        if game_state.current_gas < game_state.gas_capacity:
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

