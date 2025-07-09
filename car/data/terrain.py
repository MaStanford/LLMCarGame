from .pickups import PICKUP_REPAIR, PICKUP_GAS

# --- Terrain Types ---
# Road char is '▓' (DARK SHADE)
# Tree char is 'T', Rubble char is '~'
TERRAIN_DATA = {
    "OFF_ROAD_DIRT": {"char": "░", "color_pair_name": "TERRAIN_OFFROAD_DIRT", "speed_modifier": 0.7, "passable": True},
    "OFF_ROAD_SAND": {"char": "░", "color_pair_name": "TERRAIN_OFFROAD_SAND", "speed_modifier": 0.65, "passable": True},
    "ROAD": {"char": "▓", "color_pair_name": "TERRAIN_ROAD", "speed_modifier": 1.0, "passable": True}, # Dark Shade character
    "BUILDING_WALL": {"char": "█", "color_pair_name": "TERRAIN_BUILDING", "speed_modifier": 0.0, "passable": False},
    "RUBBLE": {"char": "~", "color_pair_name": "TERRAIN_RUBBLE", "speed_modifier": 0.5, "passable": True}, # Tilde for rubble
    "GRASS": {"char": "⁘", "color_pair_name": "TERRAIN_GRASS", "speed_modifier": 0.8, "passable": True}, # FOUR DOT PUNCTUATION
    "GRASS_TALL": {"char": "∴", "color_pair_name": "TERRAIN_GRASS_TALL", "speed_modifier": 0.75, "passable": True}, # THEREFORE symbol
    "TREE": {"char": "T", "color_pair_name": "TERRAIN_TREE", "speed_modifier": 0.0, "passable": False}, # Simple 'T' for Tree
    "ROCK": {"char": "▲", "color_pair_name": "TERRAIN_ROCK", "speed_modifier": 0.0, "passable": False}, # Impassable Rock
    # Shops use building wall char for base, drawing handled specially
    "SHOP_REPAIR": {"char": "█", "color_pair_name": "SHOP_REPAIR", "speed_modifier": 0.0, "passable": False, "type": PICKUP_REPAIR, "is_shop": True},
    "SHOP_GAS": {"char": "█", "color_pair_name": "SHOP_GAS", "speed_modifier": 0.0, "passable": False, "type": PICKUP_GAS, "is_shop": True},
    "SHOP_AMMO": {"char": "█", "color_pair_name": "SHOP_AMMO", "speed_modifier": 0.0, "passable": False, "type": "AMMO", "is_shop": True},
}
