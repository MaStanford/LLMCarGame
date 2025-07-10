from .pickups import PICKUP_AMMO_BULLET, GUN_PICKUP_TYPES, PICKUP_AMMO_HEAVY_BULLET, PICKUP_AMMO_FUEL, PICKUP_DATA

ENEMIES_DATA = [
    {
        "name": "Bandit",
        "art": [
            "  _  ",
            " / \\ ",
            "|o.o|",
            " \\_/ ",
        ],
        "damage": 15, "durability": 40, "type": "moving", "speed": 0.25, "spawn_rate": 0.2,
        "min_dist": 30, "max_dist": 80, "drop_item": PICKUP_AMMO_BULLET, "drop_rate": 0.5, "cash_value": 10, "xp_value": 10,
        "alt_drop_items": GUN_PICKUP_TYPES, "alt_drop_rate": 0.1
    },
    {
        "name": "Rusty Sedan",
        "art": [
            "   ____   ",
            "  / __ \\  ",
            " | |  | | ",
            " | |__| | ",
            "  \\____/  ",
        ],
        "damage": 25, "durability": 80, "type": "vehicle", "speed": 0.75, "spawn_rate": 0.3,
        "min_dist": 50, "max_dist": 100, "drop_item": PICKUP_AMMO_BULLET, "drop_rate": 0.7, "cash_value": 20, "xp_value": 25,
        "alt_drop_items": [p for p in GUN_PICKUP_TYPES if PICKUP_DATA[p]['gun_key'] == 'lmg'], "alt_drop_rate": 0.1
    },
    {
        "name": "Muscle Car",
        "art": [
            "   __   ",
            "  /  \\  ",
            " |----| ",
            " |    | ",
            "  \\__/  ",
        ],
        "damage": 40, "durability": 100, "type": "vehicle", "speed": 1.25, "spawn_rate": 0.15,
        "min_dist": 70, "max_dist": 120, "drop_item": PICKUP_AMMO_HEAVY_BULLET, "drop_rate": 0.6, "cash_value": 50, "xp_value": 50,
        "alt_drop_items": [p for p in GUN_PICKUP_TYPES if PICKUP_DATA[p]['gun_key'] == 'hmg'], "alt_drop_rate": 0.15
    },
    {
        "name": "Armored Truck",
        "art": [
            "   /---\\",
            "  /____\\",
            " |[][][]|",
            " (o)__(o)",
        ],
        "damage": 60, "durability": 250, "type": "vehicle", "speed": 0.5, "spawn_rate": 0.05,
        "min_dist": 100, "max_dist": 150, "drop_item": PICKUP_AMMO_FUEL, "drop_rate": 0.8, "cash_value": 100, "xp_value": 100,
        "alt_drop_items": [p for p in GUN_PICKUP_TYPES if PICKUP_DATA[p]['gun_key'] == 'flamethrower'], "alt_drop_rate": 0.2
    }
]
