from .pickups import PICKUP_REPAIR, PICKUP_GAS

BUILDING_DATA = {
    "mechanic_shop": {
        "name": "Mechanic Shop",
        "shop_type": "mechanic",
        "art": [
            "╔════════════════╗",
            "║   AUTO REPAIR  ║",
            "╠═════(>--<)═════╣",
            "║████████████████║",
            "║████████████████║",
            "║████████████████║",
            "║      ████      ║",
            "╚══════████══════╝"
        ],
        "width": 18, "height": 8,
        "color_pair_name": "SHOP_REPAIR"
    },
    "gas_station": {
        "name": "Gas Station",
        "shop_type": "gas",
        "art": [
            "    .--''''--.    ",
            "   /   G A S   \\  ",
            "  /____________\\  ",
            "       |  |       ",
            "    [#]|  | $3.59 ",
            "    [#]|  |~~~>   ",
            "    [#]|  |       "
        ],
        "width": 18, "height": 7,
        "color_pair_name": "SHOP_GAS"
    },
    "weapon_shop": {
        "name": "Ammo Shop",
        "shop_type": "weapon",
        "art": [
            "╔════════════╗",
            "║  * AMMO *  ║",
            "╠════════════╣",
            "║  * GUNS *  ║",
            "║ ╔════════╗ ║",
            "║ ║ ((O))  ║ ║",
            "║ ╚════════╝ ║",
            "╚════════════╝",
        ],
        "width": 14, "height": 7,
        "color_pair_name": "SHOP_AMMO"
    },
    "city_hall": {
        "name": "City Hall",
        "art": [
            "      /▲\\      ",
            "     /:::\\     ",
            "    /:::::\\    ",
            " ╔═══════════╗ ",
            " ║   CITY    ║ ",
            " ║   HALL    ║ ",
            " ╠═══════════╣ ",
            " ║ |o|   |o| ║ ",
            " ║ |o|   |o| ║ ",
            " ╠═════╤═════╣ ",
            " ║   ┌─┴─┐   ║ ",
            " ║   │ ■ │   ║ ",
            " ║   │   │   ║ ",
            " ║   └─┬─┘   ║ ",
            " ╚═════╧═════╝ "
        ],
        "width": 15, "height": 1,
        "color_pair_name": "BUILDING_OUTLINE_COLOR"
    }
}
