from .pickups import PICKUP_GAS, PICKUP_AMMO_BULLET, PICKUP_REPAIR, GUN_PICKUP_TYPES

OBSTACLE_DATA = [
    {
        "name": "Rock",
        "art": [
            "  /\\  ",
            " /  \\ ",
            "/____\\",
        ],
        "damage": 20, "durability": 50, "type": "static", "speed": 0, "spawn_rate": 0.5,
        "min_dist": 10, "max_dist": 50, "drop_item": None, "drop_rate": 0, "cash_value": 0, "xp_value": 2
    },
    {
        "name": "Oil Barrel",
        "art": [
            " ___ ",
            "|   |",
            "|___|",
        ],
        "damage": 10, "durability": 15, "type": "static", "speed": 0, "spawn_rate": 0.3,
        "min_dist": 20, "max_dist": 60, "drop_item": PICKUP_GAS, "drop_rate": 0.2, "cash_value": 5, "xp_value": 5
    },
]

TOTAL_SPAWN_RATE = sum(o["spawn_rate"] for o in OBSTACLE_DATA)
