def get_enemy_scaling(game_state):
    """
    Computes (hp_mult, dmg_mult, reward_mult) for enemy stat scaling
    based on player progression.

    - level_factor: +4% per player level (primary driver)
    - quest_factor: +1.5% per quest completed
    - rep_factor: +0.1% per point of best faction reputation
    - faction_bonus: +15% per defeated faction (additive)

    HP scales at full rate, damage at half rate.
    Reward scaling matches HP so tougher enemies are worth more.
    """
    level_factor = 1.0 + (game_state.player_level - 1) * 0.04
    quest_factor = 1.0 + getattr(game_state, 'quests_completed', 0) * 0.015

    max_rep = max(game_state.faction_reputation.values(), default=0)
    max_rep = max(0, max_rep)  # Ignore negative rep
    rep_factor = 1.0 + max_rep * 0.001

    defeated_count = len(game_state.defeated_bosses)
    faction_bonus = 0.15 * defeated_count

    hp_mult = level_factor * quest_factor * rep_factor + faction_bonus
    dmg_mult = 1.0 + (hp_mult - 1.0) * 0.5
    reward_mult = hp_mult

    return hp_mult, dmg_mult, reward_mult
