import random
from ..data.modifiers import WEAPON_MODIFIERS

def generate_weapon_modifiers(base_weapon_key, player_level, town_reputation, drop_chance_modifier=1.0):
    """
    Generates a dictionary of modifiers for a weapon based on various factors.
    """
    modifiers = {}
    
    # Determine the number of modifiers to apply
    num_modifiers = 0
    if random.random() < 0.2 * drop_chance_modifier:
        num_modifiers = 1
    if random.random() < 0.05 * drop_chance_modifier:
        num_modifiers = 2
    if random.random() < 0.01 * drop_chance_modifier:
        num_modifiers = 3
        
    if num_modifiers == 0:
        return modifiers
        
    # Determine the rarity of the modifiers
    rarity = "common"
    if random.random() < 0.15 * drop_chance_modifier:
        rarity = "rare"
    if random.random() < 0.05 * drop_chance_modifier:
        rarity = "legendary"
        
    # Apply the modifiers
    for _ in range(num_modifiers):
        modifier_key = random.choice(list(WEAPON_MODIFIERS.keys()))
        
        if modifier_key in WEAPON_MODIFIERS and rarity in WEAPON_MODIFIERS[modifier_key]:
            min_boost, max_boost = WEAPON_MODIFIERS[modifier_key][rarity]
            
            # Add a small boost based on player level and town reputation
            level_boost = (player_level / 100) * (max_boost - min_boost)
            rep_boost = (town_reputation / 200) * (max_boost - min_boost)
            
            boost = random.uniform(min_boost, max_boost) + level_boost + rep_boost
            
            modifiers[modifier_key] = boost
            
    return modifiers
