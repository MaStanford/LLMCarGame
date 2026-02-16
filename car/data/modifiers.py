# --- Weapon Modifier Definitions ---

RARITY_TIERS = {
    "common": {"color": "white", "weight": 75},
    "uncommon": {"color": "green", "weight": 15},
    "rare": {"color": "blue", "weight": 6},
    "epic": {"color": "purple", "weight": 3},
    "legendary": {"color": "orange", "weight": 1}
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

# --- Equipment Modifier Definitions ---

EQUIPMENT_MODIFIER_POOLS = {
    "common": {
        "durability_boost": (1.01, 1.05),
        "speed_boost": (1.01, 1.05),
    },
    "uncommon": {
        "durability_boost": (1.06, 1.10),
        "speed_boost": (1.06, 1.10),
        "handling_boost": (1.01, 1.05),
    },
    "rare": {
        "durability_boost": (1.11, 1.15),
        "speed_boost": (1.11, 1.15),
        "handling_boost": (1.06, 1.10),
        "fuel_efficiency_boost": (1.05, 1.10),
    },
    "epic": {
        "durability_boost": (1.16, 1.20),
        "speed_boost": (1.16, 1.20),
        "handling_boost": (1.11, 1.15),
        "fuel_efficiency_boost": (1.10, 1.15),
    },
    "legendary": {
        "durability_boost": (1.21, 1.25),
        "speed_boost": (1.21, 1.25),
        "handling_boost": (1.16, 1.20),
        "fuel_efficiency_boost": (1.15, 1.25),
    }
}
