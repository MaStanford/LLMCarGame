# This file defines the possible modifiers that can be applied to weapons.
# The structure is:
# "modifier_key": {
#     "rarity": (min_boost, max_boost)
# }

WEAPON_MODIFIERS = {
    "damage_boost": {
        "common": (1.05, 1.1),
        "rare": (1.15, 1.25),
        "legendary": (1.3, 1.5)
    },
    "fire_rate_boost": {
        "common": (0.9, 0.95), # Lower is better for fire rate
        "rare": (0.8, 0.85),
        "legendary": (0.7, 0.75)
    },
    "range_boost": {
        "common": (1.1, 1.2),
        "rare": (1.25, 1.4),
        "legendary": (1.5, 1.75)
    },
    "pellet_count_boost": {
        "common": (1, 2),
        "rare": (2, 3),
        "legendary": (3, 5)
    }
}
