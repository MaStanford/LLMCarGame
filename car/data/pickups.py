# --- Ammo Types ---
AMMO_BULLET = "BULLET"
AMMO_HEAVY_BULLET = "HEAVY_BULLET"
AMMO_FUEL = "FUEL"
AMMO_MINES = "MINES"

# --- Pickup Types ---
PICKUP_GAS = "GAS"
PICKUP_AMMO_BULLET = "AMMO_BULLET"
PICKUP_AMMO_HEAVY = "AMMO_HEAVY"
PICKUP_AMMO_FUEL = "AMMO_FUEL"
PICKUP_AMMO_MINES = "AMMO_MINES"
PICKUP_REPAIR = "REPAIR"
PICKUP_CASH = "CASH"
PICKUP_GUN_LMG = "GUN_LMG"     # New Gun Pickups
PICKUP_GUN_HMG = "GUN_HMG"
PICKUP_GUN_FLAMER = "GUN_FLAMER"
PICKUP_GUN_MINE_LAUNCHER = "GUN_MINE_LAUNCHER"

# Replaced emojis in pickup data, added guns
PICKUP_DATA = {
    PICKUP_GAS: {"art": ["F"], "color_pair_name": "PICKUP_GAS", "value": 500},
    PICKUP_AMMO_BULLET: {"art": ["B"], "color_pair_name": "PICKUP_AMMO", "value": 50, "ammo_type": AMMO_BULLET},
    PICKUP_AMMO_HEAVY: {"art": ["H"], "color_pair_name": "PICKUP_AMMO", "value": 25, "ammo_type": AMMO_HEAVY_BULLET},
    PICKUP_AMMO_FUEL: {"art": ["f"], "color_pair_name": "PICKUP_AMMO", "value": 100, "ammo_type": AMMO_FUEL},
    PICKUP_AMMO_MINES: {"art": ["M"], "color_pair_name": "PICKUP_AMMO", "value": 5, "ammo_type": AMMO_MINES},
    PICKUP_REPAIR: {"art": ["R"], "color_pair_name": "PICKUP_REPAIR", "value": 25},
    PICKUP_CASH: {"art": ["$"], "color_pair_name": "PICKUP_CASH", "value": 10},
    PICKUP_GUN_LMG: {"art": ["LMG"], "color_pair_name": "PICKUP_GUN", "gun_key": "lmg"}, # Gun pickups
    PICKUP_GUN_HMG: {"art": ["HMG"], "color_pair_name": "PICKUP_GUN", "gun_key": "hmg"},
    PICKUP_GUN_FLAMER: {"art": ["FLM"], "color_pair_name": "PICKUP_GUN", "gun_key": "flamethrower"},
    PICKUP_GUN_MINE_LAUNCHER: {"art": ["MIN"], "color_pair_name": "PICKUP_GUN", "gun_key": "mine_launcher"},
}
GUN_PICKUP_TYPES = [PICKUP_GUN_LMG, PICKUP_GUN_HMG, PICKUP_GUN_FLAMER, PICKUP_GUN_MINE_LAUNCHER]
