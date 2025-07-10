# --- Difficulty Levels ---
DIFFICULTY_LEVELS = ["Easy", "Normal", "Hard", "Very Hard"]
DIFFICULTY_MODIFIERS = {
    "Easy": {"enemy_hp_mult": 0.7, "enemy_dmg_mult": 0.7, "spawn_rate_mult": 0.8, "xp_mult": 1.2, "starting_cash": 500, "max_enemies": 5},
    "Normal": {"enemy_hp_mult": 1.0, "enemy_dmg_mult": 1.0, "spawn_rate_mult": 1.0, "xp_mult": 1.0, "starting_cash": 300, "max_enemies": 7},
    "Hard": {"enemy_hp_mult": 1.5, "enemy_dmg_mult": 1.3, "spawn_rate_mult": 1.2, "xp_mult": 0.8, "starting_cash": 200, "max_enemies": 8},
    "Very Hard": {"enemy_hp_mult": 2.0, "enemy_dmg_mult": 1.8, "spawn_rate_mult": 1.5, "xp_mult": 0.6, "starting_cash": 100, "max_enemies": 10},
}
