# --- Weapon Modifier Definitions ---

RARITY_TIERS = {
    "common": {"color": "white", "weight": 85},
    "uncommon": {"color": "green", "weight": 10},
    "rare": {"color": "blue", "weight": 4.85},
    "epic": {"color": "purple", "weight": 0.10},
    "legendary": {"color": "orange", "weight": 0.05}
}

MODIFIER_POOLS = {
    "common": {
        "damage_boost": (1.01, 1.05),
        "fire_rate_boost": (1.01, 1.05),
    },
    "uncommon": {
        "damage_boost": (1.06, 1.10),
        "fire_rate_boost": (1.06, 1.10),
        "range_boost": (1.01, 1.05),
    },
    "rare": {
        "damage_boost": (1.11, 1.15),
        "fire_rate_boost": (1.11, 1.15),
        "range_boost": (1.06, 1.10),
        "pellet_count_boost": (1, 2),
    },
    "epic": {
        "damage_boost": (1.16, 1.20),
        "fire_rate_boost": (1.16, 1.20),
        "range_boost": (1.11, 1.15),
        "pellet_count_boost": (2, 3),
    },
    "legendary": {
        "damage_boost": (1.21, 1.25),
        "fire_rate_boost": (1.21, 1.25),
        "range_boost": (1.16, 1.20),
        "pellet_count_boost": (3, 4),
        "special_effect": ["explosive_rounds", "vampire_rounds"]
    }
}
