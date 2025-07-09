from .pickups import PICKUP_GAS, PICKUP_AMMO_BULLET, PICKUP_REPAIR, GUN_PICKUP_TYPES

# --- Obstacle Definitions ---
# Added xp_value to obstacles
OBSTACLE_DATA = [
    {"name": "Oil Barrel", "art": ["╭─╮","│O│","╰─╯"], "damage": 10, "durability": 15, "type": "static", "speed": 0, "spawn_rate": 0.3, "min_dist": 20, "max_dist": 60, "drop_item": PICKUP_GAS, "drop_rate": 0.2, "cash_value": 5, "xp_value": 5},
    {"name": "Dumpster", "art": ["╔═╗","║D║","╚═╝"], "damage": 20, "durability": 30, "type": "static", "speed": 0, "spawn_rate": 0.2, "min_dist": 30, "max_dist": 70, "drop_item": PICKUP_AMMO_BULLET, "drop_rate": 0.15, "cash_value": 10, "xp_value": 10},
    {"name": "Broken Car", "art": ["╭=╮","║W║","╰=╯"], "damage": 30, "durability": 50, "type": "static", "speed": 0, "spawn_rate": 0.1, "min_dist": 40, "max_dist": 80,
     "drop_item": PICKUP_REPAIR, "drop_rate": 0.2,
     "alt_drop_items": GUN_PICKUP_TYPES, "alt_drop_rate": 0.15,
     "cash_value": 20, "xp_value": 15},
    {"name": "Dog", "art": [" d ","~^~"], "damage": 5, "durability": 5, "type": "moving", "speed": 0.2, "spawn_rate": 0.2, "min_dist": 15, "max_dist": 50, "drop_item": None, "drop_rate": 0, "cash_value": -5, "xp_value": 3},
    {"name": "Zombie", "art": [" Z ","~*~"], "damage": 15, "durability": 10, "type": "moving", "speed": 0.1, "spawn_rate": 0.2, "min_dist": 25, "max_dist": 60, "drop_item": PICKUP_AMMO_BULLET, "drop_rate": 0.05, "cash_value": 15, "xp_value": 8},
]

# Calculate total spawn rate for normalization
TOTAL_SPAWN_RATE = sum(o["spawn_rate"] for o in OBSTACLE_DATA)
