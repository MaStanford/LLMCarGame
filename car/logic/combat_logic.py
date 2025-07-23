import random

def player_turn(game_state, action):
    """
    Resolves the player's combat action.
    Returns a log of the events that occurred.
    """
    log = []
    player = game_state.player_car
    enemy = game_state.combat_enemy

    if action == "fire":
        for weapon in game_state.mounted_weapons.values():
            if weapon:
                # Simplified hit chance
                if random.random() < 0.8: # 80% hit chance
                    damage = weapon.damage
                    enemy.durability -= damage
                    log.append(f"Your {weapon.name} hits for {damage} damage!")
                else:
                    log.append(f"Your {weapon.name} misses!")
    
    elif action == "flee":
        # Simplified flee chance
        if random.random() < 0.5: # 50% flee chance
            log.append("You successfully escaped!")
            game_state.menu_open = False
            # The screen will be popped by the UI
        else:
            log.append("You failed to escape!")

    return log

def enemy_turn(game_state):
    """
    Resolves the enemy's combat action.
    Returns a log of the events that occurred.
    """
    log = []
    player = game_state.player_car
    enemy = game_state.combat_enemy

    # Simple AI: always attack
    # (This will be expanded to use the phase system)
    if random.random() < 0.7: # 70% hit chance
        damage = getattr(enemy, "collision_damage", 10)
        player.durability -= damage
        log.append(f"The {enemy.name} hits you for {damage} damage!")
    else:
        log.append(f"The {enemy.name} misses!")

    return log

def check_combat_end(game_state):
    """
    Checks if the combat has ended and returns the result.
    """
    if game_state.combat_enemy.durability <= 0:
        return "victory"
    if game_state.player_car.durability <= 0:
        return "defeat"
    return None
