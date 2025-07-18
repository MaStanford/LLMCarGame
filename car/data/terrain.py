from rich.style import Style

TERRAIN_DATA_RAW = {
    "OFF_ROAD_DIRT": {"char": "░", "style": "rgb(139,69,19)", "speed_modifier": 0.7, "passable": True},
    "OFF_ROAD_SAND": {"char": "░", "style": "rgb(244,164,96)", "speed_modifier": 0.65, "passable": True},
    "ROAD": {"char": "▓", "style": "white on rgb(40,40,40)", "speed_modifier": 1.0, "passable": True},
    "BUILDING_WALL": {"char": "█", "style": "white on black", "speed_modifier": 0.0, "passable": False},
    "RUBBLE": {"char": "~", "style": "rgb(139,139,131) on black", "speed_modifier": 0.5, "passable": True},
    "GRASS": {"char": "⁘", "style": "green on rgb(0,50,0)", "speed_modifier": 0.8, "passable": True},
    "GRASS_TALL": {"char": "∴", "style": "green on rgb(0,40,0)", "speed_modifier": 0.75, "passable": True},
    "TREE": {"char": "T", "style": "green", "speed_modifier": 0.0, "passable": False},
    "ROCK": {"char": "▲", "style": "bright_black", "speed_modifier": 0.0, "passable": False},
    "SHOP_REPAIR": {"char": "█", "style": "white on blue", "speed_modifier": 0.0, "passable": False, "type": "REPAIR", "is_shop": True},
    "SHOP_GAS": {"char": "█", "style": "white on red", "speed_modifier": 0.0, "passable": False, "type": "GAS", "is_shop": True},
    "SHOP_AMMO": {"char": "█", "style": "white on cyan", "speed_modifier": 0.0, "passable": False, "type": "AMMO", "is_shop": True},
}

# Pre-parse the styles for performance
TERRAIN_DATA = {
    key: {**value, "style": Style.parse(value["style"])}
    for key, value in TERRAIN_DATA_RAW.items()
}

