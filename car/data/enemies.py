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
        "alt_drop_items": GUN_PICKUP_TYPES, "alt_drop_rate": 0.1,
        "phases": [
            {"name": "Charge", "duration": (3, 5), "behavior": "CHASE", "next_phases": {"Charge": 0.8, "Hesitate": 0.2}},
            {"name": "Hesitate", "duration": (1, 2), "behavior": "STATIONARY", "next_phases": {"Charge": 1.0}}
        ]
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
        "alt_drop_items": [p for p in GUN_PICKUP_TYPES if PICKUP_DATA[p]['gun_key'] == 'lmg'], "alt_drop_rate": 0.1,
        "phases": [
            {"name": "Pursuit", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"DriveBy": 1.0}},
            {"name": "DriveBy", "duration": (3, 5), "behavior": "STRAFE", "next_phases": {"Pursuit": 0.7, "Reposition": 0.3}},
            {"name": "Reposition", "duration": (2, 3), "behavior": "EVADE", "next_phases": {"Pursuit": 1.0}}
        ]
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
        "alt_drop_items": [p for p in GUN_PICKUP_TYPES if PICKUP_DATA[p]['gun_key'] == 'hmg'], "alt_drop_rate": 0.15,
        "phases": [
            {"name": "AggressiveChase", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"StrafeAndShoot": 1.0}},
            {"name": "StrafeAndShoot", "duration": (4, 6), "behavior": "STRAFE", "next_phases": {"AggressiveChase": 0.7, "RammingRun": 0.3}},
            {"name": "RammingRun", "duration": (2, 3), "behavior": "RAM", "next_phases": {"AggressiveChase": 1.0}}
        ]
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
        "alt_drop_items": [p for p in GUN_PICKUP_TYPES if PICKUP_DATA[p]['gun_key'] == 'flamethrower'], "alt_drop_rate": 0.2,
        "phases": [
            {"name": "ProbingAttack", "duration": (5, 7), "behavior": "CHASE", "next_phases": {"ProbingAttack": 1.0}},
        ]
    }
]
