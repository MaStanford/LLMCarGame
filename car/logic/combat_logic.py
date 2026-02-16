import random
import math

# --- Boss Combat Phase Definitions ---
BOSS_PHASES = [
    {
        "name": "Charging",
        "duration": 2,
        "telegraph": "is revving its engine!",
        "tip": "Evade to dodge the charge!",
        "damage_key": "collision_damage",
        "damage_mult": 2.0,
        "hit_chance": 0.6,
    },
    {
        "name": "Firing",
        "duration": 2,
        "telegraph": "takes aim at you!",
        "tip": "Defend to reduce incoming fire!",
        "damage_key": "shoot_damage",
        "damage_mult": 1.0,
        "hit_chance": 0.8,
    },
    {
        "name": "Exposed",
        "duration": 2,
        "telegraph": "is overheated and exposed!",
        "tip": "Fire now for bonus damage!",
        "damage_key": "shoot_damage",
        "damage_mult": 0.5,
        "hit_chance": 0.5,
    },
    {
        "name": "Recovering",
        "duration": 1,
        "telegraph": "is catching its breath.",
        "tip": "Free opportunity to attack!",
        "damage_key": "collision_damage",
        "damage_mult": 0.3,
        "hit_chance": 0.4,
    },
]


def get_current_phase(game_state):
    """Returns the current boss combat phase dict."""
    idx = getattr(game_state, 'boss_phase_index', 0)
    return BOSS_PHASES[idx % len(BOSS_PHASES)]


def _calculate_weapon_damage(game_state):
    """Calculate total damage from all mounted weapons, respecting pellet count and level scaling."""
    total = 0
    log = []
    dmg_modifier = getattr(game_state, 'level_damage_modifier', 1.0)

    for weapon in game_state.mounted_weapons.values():
        if weapon is None:
            continue
        pellets = getattr(weapon, 'pellet_count', 1)
        per_pellet_accuracy = 0.8 if pellets == 1 else 0.6

        hits = 0
        for _ in range(pellets):
            if random.random() < per_pellet_accuracy:
                hits += 1

        if hits > 0:
            raw_damage = weapon.damage * hits
            scaled_damage = max(1, int(raw_damage * dmg_modifier))
            total += scaled_damage
            if pellets > 1:
                log.append(f"  {weapon.name}: {hits}/{pellets} pellets hit for {scaled_damage} damage!")
            else:
                log.append(f"  {weapon.name} hits for {scaled_damage} damage!")
        else:
            log.append(f"  {weapon.name} misses!")

    return total, log


def player_turn(game_state, action):
    """
    Resolves the player's combat action.
    Returns (log_lines, fled_successfully).
    """
    log = []
    enemy = game_state.combat_enemy
    phase = get_current_phase(game_state)

    # Reset defensive flags
    game_state.player_defending = False
    game_state.player_evading = False

    if action == "fire":
        damage, weapon_log = _calculate_weapon_damage(game_state)

        # Bonus damage during Exposed phase
        if phase["name"] == "Exposed":
            damage = int(damage * 1.5)
            log.append("You exploit the opening! (1.5x damage)")

        if damage > 0:
            enemy.durability -= damage
            log.append(f"You fire your weapons for {damage} total damage!")
            log.extend(weapon_log)
        else:
            log.append("All your shots miss!")
            log.extend(weapon_log)

    elif action == "defend":
        game_state.player_defending = True
        # Counter damage at 25% power
        damage, _ = _calculate_weapon_damage(game_state)
        counter_damage = max(1, damage // 4)
        enemy.durability -= counter_damage
        log.append(f"You brace for impact and counter for {counter_damage} damage!")

    elif action == "evade":
        game_state.player_evading = True
        # Counterattack on successful evasion during Charging
        if phase["name"] == "Charging":
            damage, _ = _calculate_weapon_damage(game_state)
            counter_damage = max(1, damage // 2)
            enemy.durability -= counter_damage
            log.append(f"You dodge the charge and counterattack for {counter_damage} damage!")
        else:
            log.append("You prepare to evade!")

    elif action == "flee":
        player_speed = getattr(game_state, 'max_speed', 10)
        enemy_speed = getattr(enemy, 'speed', 5)
        flee_chance = min(0.8, max(0.2, player_speed / (player_speed + enemy_speed)))
        if random.random() < flee_chance:
            log.append("You successfully escaped!")
            game_state.menu_open = False
            return log, True  # fled successfully
        else:
            log.append("You failed to escape!")

    return log, False


def enemy_turn(game_state):
    """
    Resolves the enemy's combat action based on current boss phase.
    Advances phase timer afterward.
    Returns log lines.
    """
    log = []
    enemy = game_state.combat_enemy
    phase = get_current_phase(game_state)

    base_damage = getattr(enemy, phase["damage_key"], 10)
    damage = max(1, int(base_damage * phase["damage_mult"]))
    hit_chance = phase["hit_chance"]

    # Check player defensive actions
    if game_state.player_evading:
        if phase["name"] == "Charging":
            # Auto-dodge during charging
            log.append(f"The {enemy.name} charges but you dodge completely!")
            damage = 0
        else:
            # Handling-based dodge chance
            handling = getattr(game_state.player_car, 'handling', 0.5)
            dodge_chance = min(0.7, handling * 0.8)
            if random.random() < dodge_chance:
                log.append(f"You evade the {enemy.name}'s attack!")
                damage = 0
            else:
                log.append(f"You fail to evade!")

    if damage > 0:
        if random.random() < hit_chance:
            if game_state.player_defending:
                damage = max(1, damage // 2)
                log.append(f"The {enemy.name} hits, but your defense reduces it to {damage} damage!")
            else:
                log.append(f"The {enemy.name} hits you for {damage} damage!")
            game_state.current_durability -= damage
        else:
            log.append(f"The {enemy.name} misses!")

    # Reset defensive flags
    game_state.player_defending = False
    game_state.player_evading = False

    # Advance phase timer
    game_state.boss_phase_turns -= 1
    if game_state.boss_phase_turns <= 0:
        game_state.boss_phase_index = (game_state.boss_phase_index + 1) % len(BOSS_PHASES)
        next_phase = BOSS_PHASES[game_state.boss_phase_index]
        game_state.boss_phase_turns = next_phase["duration"]
        log.append(f"")
        log.append(f"The {enemy.name} {next_phase['telegraph']}")

    return log


def check_combat_end(game_state):
    """Checks if the combat has ended and returns the result."""
    if game_state.combat_enemy.durability <= 0:
        return "victory"
    if game_state.current_durability <= 0:
        return "defeat"
    return None
