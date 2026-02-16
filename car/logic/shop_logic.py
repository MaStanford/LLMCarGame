from ..data.weapons import WEAPONS_DATA
from ..data.equipment import EQUIPMENT_DATA
from ..data.pickups import (
    AMMO_BULLET, AMMO_HEAVY_BULLET, AMMO_SHOTGUN, AMMO_MINES, AMMO_FUEL,
)
from ..data.modifiers import (
    RARITY_PRICE_MULTIPLIERS, RARITY_STAT_MULTIPLIERS, RARITY_REP_THRESHOLDS, RARITY_ORDER,
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
        weapon = Weapon(
            item["item_id"],
            modifiers=item.get("modifiers", {}),
            rarity=item.get("rarity", "common"),
        )
        game_state.player_inventory.append(weapon)
    elif item_type == "equipment":
        equipment = Equipment(
            item["item_id"],
            modifiers=item.get("modifiers", {}),
            rarity=item.get("rarity", "common"),
        )
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


def _get_unlocked_rarities(game_state, faction_id):
    """Returns the list of rarity tiers unlocked by the player's reputation with this faction."""
    local_rep = game_state.faction_reputation.get(faction_id, 0)
    return [r for r in RARITY_ORDER if local_rep >= RARITY_REP_THRESHOLDS[r]]


def _generate_weapon_shop_entries(weapon_id, unlocked_rarities, price_modifier):
    """Generate shop entries for a weapon at each unlocked rarity."""
    entries = []
    base_weapon = Weapon(weapon_id)
    base_price = base_weapon.price
    base_name = base_weapon.name

    for rarity in unlocked_rarities:
        stat_mult = RARITY_STAT_MULTIPLIERS[rarity]
        price_mult = RARITY_PRICE_MULTIPLIERS[rarity]

        # Deterministic modifiers for shop items
        modifiers = {}
        if stat_mult > 1.0:
            modifiers["damage_boost"] = stat_mult
            modifiers["fire_rate_boost"] = round(1.0 + (stat_mult - 1.0) * 0.6, 2)
            modifiers["range_boost"] = round(1.0 + (stat_mult - 1.0) * 0.4, 2)

        display_name = f"{rarity.capitalize()} {base_name}" if rarity != "common" else base_name
        rarity_price = int(base_price * price_mult * price_modifier)

        # Compute displayed stats with modifiers applied
        displayed_damage = base_weapon.base_stats["power"] * modifiers.get("damage_boost", 1.0)
        displayed_range = base_weapon.base_stats["range"] * modifiers.get("range_boost", 1.0)
        displayed_fire_rate = base_weapon.base_stats["fire_rate"] * modifiers.get("fire_rate_boost", 1.0)

        entries.append({
            "type": "weapon",
            "name": display_name,
            "damage": round(displayed_damage, 1),
            "range": round(displayed_range, 1),
            "fire_rate": round(displayed_fire_rate, 1),
            "ammo_type": base_weapon.ammo_type,
            "price": rarity_price,
            "item_id": weapon_id,
            "modifiers": modifiers,
            "rarity": rarity,
        })
    return entries


def _generate_equipment_shop_entries(equip_id, equip_data, unlocked_rarities, price_modifier):
    """Generate shop entries for equipment at each unlocked rarity."""
    entries = []
    base_price = equip_data["price"]
    base_name = equip_data["name"]
    base_bonuses = equip_data.get("bonuses", {})

    for rarity in unlocked_rarities:
        stat_mult = RARITY_STAT_MULTIPLIERS[rarity]
        price_mult = RARITY_PRICE_MULTIPLIERS[rarity]

        # For equipment, apply stat_mult to all bonus keys
        modifiers = {}
        if stat_mult > 1.0:
            for stat_key in base_bonuses:
                modifiers[f"{stat_key}_boost"] = stat_mult

        display_name = f"{rarity.capitalize()} {base_name}" if rarity != "common" else base_name
        rarity_price = int(base_price * price_mult * price_modifier)

        # Compute displayed bonuses with modifiers applied
        displayed_bonuses = {}
        for stat_key, base_val in base_bonuses.items():
            boost_key = f"{stat_key}_boost"
            if boost_key in modifiers:
                displayed_bonuses[stat_key] = round(base_val * modifiers[boost_key], 3)
            else:
                displayed_bonuses[stat_key] = base_val

        entries.append({
            "type": "equipment",
            "name": display_name,
            "slot": equip_data["slot"],
            "description": equip_data.get("description", ""),
            "bonuses": displayed_bonuses,
            "price": rarity_price,
            "item_id": equip_id,
            "modifiers": modifiers,
            "rarity": rarity,
        })
    return entries


def get_shop_inventory(shop_type, game_state):
    """
    Gets the inventory for a given shop type, influenced by faction control and reputation.
    Higher reputation unlocks higher rarity tiers with exponentially scaled prices.
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
    if game_state.factions[local_faction_id].get("hub_city_coordinates") == (0, 0):
        price_modifier = 1.0

    # Determine which rarity tiers the player has unlocked via reputation
    unlocked_rarities = _get_unlocked_rarities(game_state, local_faction_id)

    if shop_type == "weapon_shop":
        # If faction control is too low, the shop is empty
        if faction_control < 20:
            return []

        # Sell all base weapons at unlocked rarities
        for weapon_id in WEAPONS_DATA:
            inventory.extend(_generate_weapon_shop_entries(weapon_id, unlocked_rarities, price_modifier))

        # Sell weapon-affinity equipment at unlocked rarities
        for equip_id, equip_data in EQUIPMENT_DATA.items():
            if equip_data.get("shop_affinity") == "weapon":
                inventory.extend(_generate_equipment_shop_entries(equip_id, equip_data, unlocked_rarities, price_modifier))

        # Sell ammo (no rarity variants)
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

        # Sell mechanic-affinity equipment at unlocked rarities
        for equip_id, equip_data in EQUIPMENT_DATA.items():
            if equip_data.get("shop_affinity") == "mechanic":
                inventory.extend(_generate_equipment_shop_entries(equip_id, equip_data, unlocked_rarities, price_modifier))

    elif shop_type == "gas_station":
        # Fill Tank option (only if not already at full gas)
        if game_state.current_gas < game_state.gas_capacity:
            inventory.append({"type": "gas", "name": "Fill Tank", "price": int(50 * price_modifier)})

    return inventory

def calculate_sell_price(item, game_state):
    """Calculates the sell price of an item based on rarity and player level."""
    base_price = getattr(item, 'price', 0)
    rarity = getattr(item, 'rarity', 'common')
    rarity_mult = RARITY_PRICE_MULTIPLIERS.get(rarity, 1)
    level_modifier = 1.0 + (game_state.player_level * 0.05)

    # Sell price is 40% of rarity-scaled base price
    sell_price = int(base_price * rarity_mult * 0.4 * level_modifier)
    return max(1, sell_price)
