import string
from .pickups import PICKUP_REPAIR, PICKUP_GAS

# --- Shop Definitions ---
# Replaced emojis in shop art
SHOP_DATA = {
    "REPAIR": {
        "name": "Repair Shop",
        "art": [
            "╔════════════════╗",
            "║  ===GARAGE===  ║", # Simple text/symbols
            "║┌─┬─┬─┬┐ R  ║",
            "║├─┼─┼─┼┤ E  ║",
            "║└─┴─┴─┴┘ P  ║",
            "╚════════════════╝",
        ],
        "width": 18, "height": 6,
        "interaction_type": PICKUP_REPAIR,
        "color_pair_name": "SHOP_REPAIR"
    },
    "GAS": {
        "name": "Gas Station",
        "art": [
            "  ╔═══════╗  ",
            " ╔╝_______╚╗ ",
            "║ | PUMP  | ║", # Text instead of emoji
            "║ | G A S | ║",
            "║ |_______| ║",
            "╚══════════��╝",
        ],
        "width": 13, "height": 6,
        "interaction_type": PICKUP_GAS,
        "color_pair_name": "SHOP_GAS"
    },
    "AMMO": {
        "name": "Ammo Shop",
        "art": [
            " ╔════════════╗ ",
            "║  * AMMO * ║", # Simple text/symbols
            "║╔═══════╗   ║",
            "║║ GUN>║   ║ ║",
            "║╚═══════╝ ║ ║",
            "╚════════════╝",
        ],
        "width": 14, "height": 6,
        "interaction_type": "AMMO", # Special type
        "color_pair_name": "SHOP_AMMO"
    },
    "CITY_HALL": {
        "name": "City Hall",
        "art": [
            "  /\\ ",
            " /  \\ ",
            "|----|",
            "| [] |",
            "|----|",
        ],
        "width": 6, "height": 5,
        "interaction_type": "QUEST",
        "color_pair_name": "BUILDING_OUTLINE_COLOR"
    }
}

# --- Building Aesthetics ---
BUILDING_OUTLINE = { # Double line characters
    "topLeft": '╔', "topRight": '╗', "bottomLeft": '╚', "bottomRight": '╝',
    "vertical": '║', "horizontal": '═'
}
# Added more symbols, removed some confusing ones
BUILDING_NAME_CHARS = string.ascii_uppercase + string.digits + "!#$%&*+=?☆★♥♦♣♠♪♫☼►◄▲▼"
