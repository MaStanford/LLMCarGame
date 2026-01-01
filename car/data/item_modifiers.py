# --- Rarity Levels ---
# Defines the rarity tiers for items and their associated colors.
RARITY_LEVELS = {
    "common": "white",
    "uncommon": "green",
    "rare": "blue",
    "epic": "purple",
    "legendary": "orange"
}

# --- Stat Modifiers ---
# Defines the possible stat modifications for items and their min/max ranges.
# These values are multipliers. For example, a "speed" of 1.2 means 20% faster.
STAT_MODIFIERS = {
    # Vehicle Stats
    "durability": [0.8, 1.5],
    "speed": [0.8, 1.5],
    "handling": [0.8, 1.5],
    "fuel_efficiency": [0.7, 1.3],

    # Weapon Stats
    "damage": [0.8, 1.5],
    "fire_rate": [0.7, 1.3], # Lower is faster
    "projectile_speed": [0.9, 1.5],
    "ammo_capacity": [0.8, 1.5]
}

# --- Cosmetic Tags ---
# A list of purely visual tags that can be applied to items.
# These are used by the LLM to add thematic flavor to generated items.
COSMETIC_TAGS = [
    "rust", "spikes", "skulls", "flames", "checkered", "custom_paint",
    "reinforced", "streamlined", "scavenged", "makeshift", "pristine",
    "corporate_logos", "military_camo", "gang_colors", "tribal_markings",
    "hazard_stripes"
]