# --- Game Constants ---
FLAME_CHAR = "~"
SHOP_INTERACTION_SPEED_THRESHOLD = 0.1

# --- World Generation ---
CITY_SPACING = 500
CITY_SIZE = 100
MIN_BUILDINGS_PER_CITY = 4
MAX_BUILDINGS_PER_CITY = 12
MIN_BUILDING_DIM = 8
MAX_BUILDING_DIM = 15
ROAD_WIDTH = 15
BUILDING_SHOP_BUFFER = 2

# --- SFX MIDI Notes (Channel 10) ---
SFX_MAP = {
    "lmg": 38,          # Acoustic Snare
    "hmg": 40,          # Electric Snare
    "flamethrower": 75, # Claves (as a hiss)
    "mine_launcher": 56,# Cowbell
    "player_hit": 48,   # High Tom
    "enemy_hit": 51,    # Ride Cymbal 1
    "explosion": 35,    # Acoustic Bass Drum
    "crash": 49,        # Crash Cymbal 1
}
