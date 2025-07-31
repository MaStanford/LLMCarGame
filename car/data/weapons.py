from .pickups import AMMO_BULLET, AMMO_HEAVY_BULLET, AMMO_FUEL, AMMO_MINES, AMMO_SHOTGUN
from .game_constants import FLAME_CHAR

# --- Weapon Definitions ---
# Using multi-character art for clearer top-down representation.
WEAPONS_DATA = {
    "wep_lmg": {
        "id": "wep_lmg",
        "name": "LMG",
        "slots": 1,
        "fire_rate": 5,
        "power": 5,
        "range": 40,
        "speed": 15,
        "ammo_type": AMMO_BULLET,
        "particle": "∙",
        "price": 500,
        "art": {
            "N":  ["╨"],
            "NE": ["╲"],
            "E":  ["╞-"],
            "SE": ["╱"],
            "S":  ["╥"],
            "SW": ["╲"],
            "W":  ["-╡"],
            "NW": ["╱"]
        }
    },
    "wep_hmg": {
        "id": "wep_hmg",
        "name": "HMG",
        "slots": 2,
        "fire_rate": 10,
        "power": 15,
        "range": 60,
        "speed": 18,
        "ammo_type": AMMO_HEAVY_BULLET,
        "particle": "■",
        "price": 1500,
        "art": {
            "N":  ["█▄"],
            "NE": ["▚"],
            "E":  ["┫="],
            "SE": ["▞"],
            "S":  ["▀█"],
            "SW": ["▚"],
            "W":  ["=┣"],
            "NW": ["▞"]
        }
    },
    "wep_flamethrower": {
        "id": "wep_flamethrower",
        "name": "Flamethrower",
        "slots": 3,
        "fire_rate": 2,
        "power": 10,
        "range": 15,
        "speed": 12,
        "ammo_type": AMMO_FUEL,
        "particle": FLAME_CHAR,
        "price": 2500,
        "art": {
            "N":  ["≈^"],
            "NE": ["╱"],
            "E":  ["≈<"],
            "SE": ["╲"],
            "S":  ["≈v"],
            "SW": ["╱"],
            "W":  [">≈"],
            "NW": ["╲"]
        }
    },
    "wep_mine_launcher": {
        "id": "wep_mine_launcher",
        "name": "Mine Launcher",
        "slots": 2,
        "fire_rate": 20,
        "power": 20,
        "range": 1,
        "speed": 0,
        "ammo_type": AMMO_MINES,
        "particle": "¤",
        "price": 1000,
        "art": {
            "N":  ["(O)"],
            "NE": ["(O)"],
            "E":  ["(O)"],
            "SE": ["(O)"],
            "S":  ["(O)"],
            "SW": ["(O)"],
            "W":  ["(O)"],
            "NW": ["(O)"]
        }
    },
    "wep_pistol": {
        "id": "wep_pistol",
        "name": "Pistol",
        "slots": 1,
        "fire_rate": 3,
        "power": 2,
        "range": 30,
        "speed": 15,
        "ammo_type": AMMO_BULLET,
        "particle": "·",
        "price": 100,
        "art": {
            "N":  ["ı"],
            "NE": ["╱"],
            "E":  ["¬"],
            "SE": ["╲"],
            "S":  ["."],
            "SW": ["╱"],
            "W":  ["⌐"],
            "NW": ["╲"]
        }
    },
    "wep_shotgun": {
        "id": "wep_shotgun",
        "name": "Shotgun",
        "slots": 2,
        "fire_rate": 15,
        "power": 5,
        "range": 20,
        "speed": 13.5,
        "ammo_type": AMMO_SHOTGUN,
        "particle": "•",
        "price": 750,
        "pellet_count": 5,
        "spread_angle": 0.5,
        "art": {
            "N":  ["╦"],
            "NE": ["╲"],
            "E":  ["╠═"],
            "SE": ["╱"],
            "S":  ["╩"],
            "SW": ["╲"],
            "W":  ["═╣"],
            "NW": ["╱"]
        }
    }
}
