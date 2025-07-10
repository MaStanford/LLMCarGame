from .pickups import PICKUP_REPAIR, PICKUP_GAS

BUILDING_DATA = {
    "mechanic_shop": {
        "name": "Mechanic Shop",
        "shop_type": "mechanic",
        "art": [
            "╔════════════════╗",
            "║  ===GARAGE===  ║",
            "║┌─┬─┬─┬┐ R  ║",
            "║├─┼─┼─┼┤ E  ║",
            "║└─┴─┴─┴┘ P  ║",
            "╚════════════════╝",
        ],
        "width": 18, "height": 6,
        "color_pair_name": "SHOP_REPAIR"
    },
    "gas_station": {
        "name": "Gas Station",
        "shop_type": "gas",
        "art": [
            "  ╔═══════╗  ",
            " ╔╝_______╚╗ ",
            "║ | PUMP  | ║",
            "║ | G A S | ║",
            "║ |_______| ║",
            "╚═══════════╝",
        ],
        "width": 13, "height": 6,
        "color_pair_name": "SHOP_GAS"
    },
    "weapon_shop": {
        "name": "Ammo Shop",
        "shop_type": "weapon",
        "art": [
            " ╔════════════╗ ",
            "║  * AMMO * ║",
            "║╔═══════╗   ║",
            "║║ GUN>║   ║ ║",
            "║╚═══════╝ ║ ║",
            "╚════════════╝",
        ],
        "width": 14, "height": 6,
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
        "color_pair_name": "BUILDING_OUTLINE_COLOR"
    }
}
