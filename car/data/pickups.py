# --- Ammo Types ---
AMMO_BULLET = "BULLET"
AMMO_HEAVY_BULLET = "HEAVY_BULLET"
AMMO_FUEL = "FUEL"
AMMO_MINES = "MINES"
AMMO_SHOTGUN = "SHELL"

# --- Pickup Types ---
PICKUP_GAS = "GAS"
PICKUP_AMMO_BULLET = "AMMO_BULLET"
PICKUP_AMMO_HEAVY_BULLET = "AMMO_HEAVY_BULLET"
PICKUP_AMMO_FUEL = "AMMO_FUEL"
PICKUP_AMMO_MINES = "AMMO_MINES"
PICKUP_AMMO_SHELL = "AMMO_SHOTGUN"
PICKUP_REPAIR = "REPAIR"
PICKUP_CASH = "CASH"
PICKUP_GUN_LMG = "GUN_LMG"    
PICKUP_GUN_HMG = "GUN_HMG"
PICKUP_GUN_FLAMER = "GUN_FLAMER"
PICKUP_GUN_MINE_LAUNCHER = "GUN_MINE_LAUNCHER"

PICKUP_DATA = {
    # --- Resources ---
    PICKUP_GAS:         {"art": ["[¬]"], "color_pair_name": "PICKUP_GAS", "value": 500},
    PICKUP_REPAIR:      {"art": ["[+]"], "color_pair_name": "PICKUP_REPAIR", "value": 25},
    PICKUP_CASH:        {"art": ["[$]"], "color_pair_name": "PICKUP_CASH", "value": 10},

    # --- Ammo Pickups ---
    PICKUP_AMMO_BULLET: {"art": ["[∙∙]"], "color_pair_name": "PICKUP_AMMO", "value": 50, "ammo_type": AMMO_BULLET},
    PICKUP_AMMO_HEAVY_BULLET: {"art": ["[■■]"], "color_pair_name": "PICKUP_AMMO", "value": 25, "ammo_type": AMMO_HEAVY_BULLET},
    PICKUP_AMMO_SHELL:  {"art": ["[▊▊]"], "color_pair_name": "PICKUP_AMMO", "value": 15, "ammo_type": AMMO_SHOTGUN},
    PICKUP_AMMO_MINES:  {"art": ["[※]"], "color_pair_name": "PICKUP_AMMO", "value": 5, "ammo_type": AMMO_MINES},
    PICKUP_AMMO_FUEL:   {"art": ["[☢]"], "color_pair_name": "PICKUP_AMMO", "value": 100, "ammo_type": AMMO_FUEL},

    # --- Gun Pickups ---
    PICKUP_GUN_LMG:     {"art": ["[︻═-]"], "color_pair_name": "PICKUP_GUN", "gun_key": "lmg"},
    PICKUP_GUN_HMG:     {"art": ["[█═=]"], "color_pair_name": "PICKUP_GUN", "gun_key": "hmg"},
    PICKUP_GUN_FLAMER:  {"art": ["[≈<O]"], "color_pair_name": "PICKUP_GUN", "gun_key": "flamethrower"},
    PICKUP_GUN_MINE_LAUNCHER: {"art": ["[O<※]"], "color_pair_name": "PICKUP_GUN", "gun_key": "mine_launcher"},
}
GUN_PICKUP_TYPES = [PICKUP_GUN_LMG, PICKUP_GUN_HMG, PICKUP_GUN_FLAMER, PICKUP_GUN_MINE_LAUNCHER]
