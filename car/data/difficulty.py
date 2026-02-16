# --- Difficulty Levels ---
DIFFICULTY_LEVELS = ["Easy", "Normal", "Hard", "Very Hard"]
DIFFICULTY_MODIFIERS = {
    "Easy": {
        "enemy_hp_mult": 0.7, "enemy_dmg_mult": 0.5, "spawn_rate_mult": 0.8,
        "xp_mult": 1.2, "starting_cash": 500, "max_enemies": 8,
        "enemy_aim_spread": 3.0,       # Multiplied against base accuracy — very inaccurate
        "enemy_movement_jitter": 0.5,  # Random offset in chase/ram steering — clumsy
        "aggression_budget": 3,        # AI aggression points per cycle of 5 phases
    },
    "Normal": {
        "enemy_hp_mult": 1.0, "enemy_dmg_mult": 0.75, "spawn_rate_mult": 1.0,
        "xp_mult": 1.0, "starting_cash": 300, "max_enemies": 12,
        "enemy_aim_spread": 1.5,
        "enemy_movement_jitter": 0.25,
        "aggression_budget": 5,
    },
    "Hard": {
        "enemy_hp_mult": 1.5, "enemy_dmg_mult": 1.0, "spawn_rate_mult": 1.2,
        "xp_mult": 0.8, "starting_cash": 200, "max_enemies": 16,
        "enemy_aim_spread": 1.0,       # Baseline accuracy
        "enemy_movement_jitter": 0.1,
        "aggression_budget": 7,
    },
    "Very Hard": {
        "enemy_hp_mult": 2.0, "enemy_dmg_mult": 2.0, "spawn_rate_mult": 1.5,
        "xp_mult": 0.6, "starting_cash": 100, "max_enemies": 22,
        "enemy_aim_spread": 0.3,       # Near-perfect aim
        "enemy_movement_jitter": 0.02, # Almost no steering error
        "aggression_budget": 10,
    },
}
