# --- Difficulty Levels ---
DIFFICULTY_LEVELS = ["Easy", "Normal", "Hard"]
DIFFICULTY_MODIFIERS = {
    "Easy": {"enemy_hp_mult": 0.7, "enemy_dmg_mult": 0.7, "spawn_rate_mult": 0.8, "xp_mult": 1.2}, # More XP on easy
    "Normal": {"enemy_hp_mult": 1.0, "enemy_dmg_mult": 1.0, "spawn_rate_mult": 1.0, "xp_mult": 1.0},
    "Hard": {"enemy_hp_mult": 1.5, "enemy_dmg_mult": 1.3, "spawn_rate_mult": 1.2, "xp_mult": 0.8}, # Less XP on hard
}
