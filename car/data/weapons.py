from .pickups import AMMO_BULLET, AMMO_HEAVY_BULLET, AMMO_FUEL
from .game_constants import FLAME_CHAR

# --- Weapon Definitions ---
WEAPONS_DATA = {
    "lmg": {
        "name": "LMG", "slots": 1, "fire_rate": 5, "power": 3, "range": 40, "speed": 1.5, "ammo_type": AMMO_BULLET, "particle": "¤"
    },
    "hmg": {
        "name": "HMG", "slots": 2, "fire_rate": 10, "power": 8, "range": 60, "speed": 2.0, "ammo_type": AMMO_HEAVY_BULLET, "particle": "●"
    },
    "flamethrower": {
        "name": "Flamethrower", "slots": 3, "fire_rate": 2, "power": 5, "range": 15, "speed": 1.0, "ammo_type": AMMO_FUEL, "particle": FLAME_CHAR
    },
    "mine_launcher": {
        "name": "Mine Launcher", "slots": 2, "fire_rate": 20, "power": 20, "range": 1, "speed": 0, "ammo_type": "AMMO_MINES", "particle": "o"
    }
}
