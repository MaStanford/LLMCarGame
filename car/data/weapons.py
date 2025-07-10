from .pickups import AMMO_BULLET, AMMO_HEAVY_BULLET, AMMO_FUEL, AMMO_MINES
from .game_constants import FLAME_CHAR

# --- Weapon Definitions ---
WEAPONS_DATA = {
    "wep_lmg": {
        "id": "wep_lmg", "name": "LMG", "slots": 1, "fire_rate": 5, "power": 3, "range": 40, "speed": 1.5, "ammo_type": AMMO_BULLET, "particle": "¤",
        "art": {
            "N": ["-"], "NE": ["/"], "E": ["|"], "SE": ["\\"], "S": ["-"], "SW": ["/"], "W": ["|"], "NW": ["\\"]
        }
    },
    "wep_hmg": {
        "id": "wep_hmg", "name": "HMG", "slots": 2, "fire_rate": 10, "power": 8, "range": 60, "speed": 2.0, "ammo_type": AMMO_HEAVY_BULLET, "particle": "●",
        "art": {
            "N": ["="], "NE": ["//"], "E": ["||"], "SE": ["\\\\"], "S": ["="], "SW": ["//"], "W": ["||"], "NW": ["\\\\"]
        }
    },
    "wep_flamethrower": {
        "id": "wep_flamethrower", "name": "Flamethrower", "slots": 3, "fire_rate": 2, "power": 5, "range": 15, "speed": 1.0, "ammo_type": AMMO_FUEL, "particle": FLAME_CHAR,
        "art": {
            "N": ["{"], "NE": ["{"], "E": ["{"], "SE": ["{"], "S": ["}"], "SW": ["}"], "W": ["}"], "NW": ["}"]
        }
    },
    "wep_mine_launcher": {
        "id": "wep_mine_launcher", "name": "Mine Launcher", "slots": 2, "fire_rate": 20, "power": 20, "range": 1, "speed": 0, "ammo_type": AMMO_MINES, "particle": "o",
        "art": {
            "N": ["T"], "NE": ["T"], "E": ["T"], "SE": ["T"], "S": ["T"], "SW": ["T"], "W": ["T"], "NW": ["T"]
        }
    },
    "wep_pistol": {
        "id": "wep_pistol", "name": "Pistol", "slots": 1, "fire_rate": 3, "power": 2, "range": 30, "speed": 2.0, "ammo_type": AMMO_BULLET, "particle": ".",
        "art": {
            "N": ["¬"], "NE": ["/"], "E": ["-"], "SE": ["\\"], "S": ["¬"], "SW": ["/"], "W": ["-"], "NW": ["\\"]
        }
    },
    "wep_shotgun": {
        "id": "wep_shotgun", "name": "Shotgun", "slots": 2, "fire_rate": 15, "power": 1, "range": 20, "speed": 1.8, "ammo_type": AMMO_BULLET, "particle": "o",
        "pellet_count": 5, "spread_angle": 0.5,
        "art": {
            "N": ["<"], "NE": ["<"], "E": ["<"], "SE": ["<"], "S": [">"], "SW": [">"], "W": [">"], "NW": [">"]
        }
    }
}
