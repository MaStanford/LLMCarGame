import random
from ..data.pickups import PICKUP_DATA, PICKUP_CASH
from ..data.weapons import WEAPONS_DATA
from .modifier_logic import generate_weapon_modifiers
from ..entities.weapon import Weapon

def handle_enemy_loot_drop(game_state, enemy):
    """
    Handles the loot drop for a defeated enemy.
    """
    # Cash Drop
    cash_dropped = int(enemy.cash_value * game_state.player_level * game_state.difficulty_mods.get("xp_mult", 1.0))
    game_state.active_pickups[game_state.next_pickup_id] = {
        "type": "cash",
        "x": enemy.x,
        "y": enemy.y,
        "value": cash_dropped,
        "char": PICKUP_DATA[PICKUP_CASH]["art"][0],
        "color": PICKUP_DATA[PICKUP_CASH]["color_pair_name"]
    }
    game_state.next_pickup_id += 1

    # Weapon Drop
    if random.random() < 0.1: # 10% chance to drop a weapon
        luck_factor = 1.0
        if hasattr(enemy, "is_boss") and enemy.is_boss:
            luck_factor = 5.0 # Bosses have a much higher chance of dropping good loot
        
        modifiers = generate_weapon_modifiers(game_state.player_level, luck_factor)
        weapon_id = random.choice(list(WEAPONS_DATA.keys()))
        weapon = Weapon(weapon_id, modifiers)
        
        game_state.active_pickups[game_state.next_pickup_id] = {
            "type": "weapon",
            "x": enemy.x + 1,
            "y": enemy.y,
            "weapon": weapon,
            "char": "W",
            "color": "PICKUP_GUN"
        }
        game_state.next_pickup_id += 1
