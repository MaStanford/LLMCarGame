from .pickups import PICKUP_GAS, PICKUP_AMMO_BULLET, PICKUP_REPAIR, GUN_PICKUP_TYPES

OBSTACLE_DATA = [
    {
        "name": "Rock",
        "art": [
            "  .--.  ",
            " /.  `\\ ",
            "(______) "
        ],
        "damage": 20, "durability": 50, "type": "static", "speed": 0, "spawn_rate": 0.5,
        "min_dist": 10, "max_dist": 50, "drop_item": None, "drop_rate": 0, "cash_value": 0, "xp_value": 2
    },
    {
        "name": "Oil Barrel",
        "art": [
            " .-----. ",
            "|=======|",
            "|   ☣   |",
            "|=======|",
            " '-----' "
        ],
        "damage": 10, "durability": 15, "type": "static", "speed": 0, "spawn_rate": 0.3,
        "min_dist": 20, "max_dist": 60, "drop_item": PICKUP_GAS, "drop_rate": 0.2, "cash_value": 5, "xp_value": 5
    },
    {
        "name": "Tire Pile",
        "art": [
            "   (O)   ",
            "  (O)(O)  ",
            " (O)(O)(O) "
        ],
        "damage": 5, "durability": 30, "type": "static", "speed": 0, "spawn_rate": 0.4,
        "min_dist": 15, "max_dist": 40, "drop_item": PICKUP_REPAIR, "drop_rate": 0.05, "cash_value": 1, "xp_value": 3
    },
    {
        "name": "Scrap Barricade",
        "art": [
            " <|#/#|#\\#|>",
            " <|#\\#|#/#|>"
        ],
        "damage": 30, "durability": 200, "type": "static", "speed": 0, "spawn_rate": 0.2,
        "min_dist": 40, "max_dist": 120, "drop_item": PICKUP_AMMO_BULLET, "drop_rate": 0.2, "cash_value": 15, "xp_value": 15
    },
    {
        "name": "Wrecked Husk",
        "art": [
            "  ▄▟▀▀▙▄  ",
            " █░███░█ ",
            "(●)▀▀▀(⎐)"
        ],
        "damage": 40, "durability": 100, "type": "static", "speed": 0, "spawn_rate": 0.1,
        "min_dist": 50, "max_dist": 100, "drop_item": PICKUP_REPAIR, "drop_rate": 0.5, "cash_value": 25, "xp_value": 20
    }
]

TOTAL_SPAWN_RATE = sum(o["spawn_rate"] for o in OBSTACLE_DATA)
