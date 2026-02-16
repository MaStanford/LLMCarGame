import random
from ..data.modifiers import RARITY_TIERS, MODIFIER_POOLS, EQUIPMENT_MODIFIER_POOLS

def generate_weapon_modifiers(player_level, luck_factor=1.0):
    """
    Generates a set of modifiers for a weapon based on player level and luck.
    """
    # Determine rarity
    rarity_weights = {rarity: data["weight"] for rarity, data in RARITY_TIERS.items()}

    # Adjust weights based on luck
    for rarity in rarity_weights:
        if rarity != "common":
            rarity_weights[rarity] *= luck_factor

    # Adjust weights for player level
    for rarity in rarity_weights:
        if rarity != "common":
            rarity_weights[rarity] *= (1 + player_level / 100)

    chosen_rarity = random.choices(list(rarity_weights.keys()), weights=list(rarity_weights.values()), k=1)[0]

    # Generate modifiers based on rarity
    modifiers = {}
    modifier_pool = MODIFIER_POOLS[chosen_rarity]

    num_modifiers = 1
    if chosen_rarity == "uncommon":
        num_modifiers = random.randint(1, 2)
    elif chosen_rarity == "rare":
        num_modifiers = random.randint(2, 3)
    elif chosen_rarity == "epic":
        num_modifiers = random.randint(3, 4)
    elif chosen_rarity == "legendary":
        num_modifiers = random.randint(4, 5)
    elif chosen_rarity == "godly":
        num_modifiers = random.randint(5, 6)

    for _ in range(num_modifiers):
        modifier_type = random.choice(list(modifier_pool.keys()))
        if modifier_type == "special_effect":
            modifiers[modifier_type] = random.choice(modifier_pool[modifier_type])
        else:
            min_val, max_val = modifier_pool[modifier_type]
            modifiers[modifier_type] = round(random.uniform(min_val, max_val), 2)

    return modifiers


def generate_equipment_modifiers(player_level, luck_factor=1.0):
    """
    Generates a set of modifiers for equipment based on player level and luck.
    Returns (modifiers_dict, rarity_string).
    """
    rarity_weights = {rarity: data["weight"] for rarity, data in RARITY_TIERS.items()}

    for rarity in rarity_weights:
        if rarity != "common":
            rarity_weights[rarity] *= luck_factor
            rarity_weights[rarity] *= (1 + player_level / 100)

    chosen_rarity = random.choices(list(rarity_weights.keys()), weights=list(rarity_weights.values()), k=1)[0]

    modifiers = {}
    modifier_pool = EQUIPMENT_MODIFIER_POOLS[chosen_rarity]

    num_modifiers = 1
    if chosen_rarity == "uncommon":
        num_modifiers = random.randint(1, 2)
    elif chosen_rarity == "rare":
        num_modifiers = random.randint(2, 3)
    elif chosen_rarity == "epic":
        num_modifiers = random.randint(3, 4)
    elif chosen_rarity == "legendary":
        num_modifiers = random.randint(4, 5)
    elif chosen_rarity == "godly":
        num_modifiers = random.randint(5, 6)

    for _ in range(num_modifiers):
        modifier_type = random.choice(list(modifier_pool.keys()))
        min_val, max_val = modifier_pool[modifier_type]
        modifiers[modifier_type] = round(random.uniform(min_val, max_val), 2)

    return modifiers, chosen_rarity
