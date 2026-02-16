# --- Rarity Tier Definitions ---

RARITY_TIERS = {
    "common": {"color": "white", "weight": 75},
    "uncommon": {"color": "green", "weight": 15},
    "rare": {"color": "blue", "weight": 6},
    "epic": {"color": "purple", "weight": 3},
    "legendary": {"color": "orange", "weight": 1},
    "godly": {"color": "red", "weight": 0.1},
}

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "godly"]

# --- Shop Rarity Scaling ---

RARITY_PRICE_MULTIPLIERS = {
    "common": 1,
    "uncommon": 3,
    "rare": 10,
    "epic": 100,
    "legendary": 10_000,
    "godly": 10_000_000,
}

RARITY_STAT_MULTIPLIERS = {
    "common": 1.0,
    "uncommon": 1.25,
    "rare": 1.6,
    "epic": 2.0,
    "legendary": 3.0,
    "godly": 4.0,
}

RARITY_REP_THRESHOLDS = {
    "common": 0,
    "uncommon": 10,
    "rare": 25,
    "epic": 50,
    "legendary": 100,
    "godly": 200,
}

# --- Weapon Modifier Pools (for loot drops) ---

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
    },
    "godly": {
        "damage_boost": (1.26, 1.35),
        "fire_rate_boost": (1.26, 1.35),
        "range_boost": (1.21, 1.30),
        "pellet_count_boost": (4, 6),
        "special_effect": ["explosive_rounds", "vampire_rounds", "piercing_rounds"]
    },
}

# --- Equipment Modifier Pools (for loot drops) ---

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
    },
    "godly": {
        "durability_boost": (1.26, 1.35),
        "speed_boost": (1.26, 1.35),
        "handling_boost": (1.21, 1.30),
        "fuel_efficiency_boost": (1.20, 1.30),
    },
}
