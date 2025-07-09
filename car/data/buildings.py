from .pickups import PICKUP_REPAIR, PICKUP_GAS

BUILDING_DATA = {
    "mechanic_shop": {
        "name": "Mechanic Shop",
        "inventory": [
            {"item": "PICKUP_REPAIR", "price": 50},
            {"item": "PICKUP_GAS", "price": 20},
        ],
        "art": [
            "╔════════════════╗",
            "║  ===GARAGE===  ║",
            "║┌─┬─┬─┬┐ R  ║",
            "║├─┼─┼─┼┤ E  ║",
            "║└─┴─┴─┴┘ P  ║",
            "╚════════════════╝",
        ],
        "width": 18, "height": 6,
        "interaction_type": PICKUP_REPAIR,
        "color_pair_name": "SHOP_REPAIR"
    },
    "gas_station": {
        "name": "Gas Station",
        "inventory": [
            {"item": "PICKUP_GAS", "price": 20},
        ],
        "art": [
            "  ╔═══════╗  ",
            " ╔╝_______╚╗ ",
            "║ | PUMP  | ║",
            "║ | G A S | ║",
            "║ |_______| ║",
            "╚═══════════╝",
        ],
        "width": 13, "height": 6,
        "interaction_type": PICKUP_GAS,
        "color_pair_name": "SHOP_GAS"
    },
    "weapon_shop": {
        "name": "Ammo Shop",
        "inventory": [
            {"item": "lmg", "price": 100},
            {"item": "hmg", "price": 200},
            {"item": "flamethrower", "price": 300},
            {"item": "mine_launcher", "price": 400},
        ],
        "art": [
            " ╔════════════╗ ",
            "║  * AMMO * ║",
            "║╔═══════╗   ║",
            "║║ GUN>║   ║ ║",
            "║╚═══════╝ ║ ║",
            "╚════════════╝",
        ],
        "width": 14, "height": 6,
        "interaction_type": "AMMO", # Special type
        "color_pair_name": "SHOP_AMMO"
    },
    "city_hall": {
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
