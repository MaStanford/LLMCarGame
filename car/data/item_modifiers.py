# car/data/item_modifiers.py

# Defines the possible stat modifiers that can be applied to weapons and vehicles.
# Each key is the stat to be modified, and the value is a tuple of (min_modifier, max_modifier).
STAT_MODIFIERS = {
    # Vehicle Stats
    "durability": (0.8, 1.5),
    "speed": (0.8, 1.5),
    "handling": (0.8, 1.5),
    "fuel_efficiency": (0.7, 1.3),

    # Weapon Stats
    "damage": (0.8, 1.5),
    "fire_rate": (0.7, 1.3), # Lower is faster
    "projectile_speed": (0.9, 1.5),
    "ammo_capacity": (0.8, 1.5),
}

# Defines the possible cosmetic tags that can be applied to items.
# These are purely descriptive and do not affect gameplay.
COSMETIC_TAGS = [
    # General
    "rust", "spikes", "skulls", "flames", "checkered", "custom_paint",
    "reinforced", "streamlined", "scavenged", "makeshift", "pristine",
    
    # Faction Specific
    "corporate_logos", "military_camo", "gang_colors", "tribal_markings",
    "hazard_stripes",
]

# Defines the rarity levels for generated items.
# Each rarity has a corresponding color for UI display.
RARITY_LEVELS = {
    "common": "white",
    "uncommon": "green",
    "rare": "blue",
    "epic": "purple",
    "legendary": "orange",
}
