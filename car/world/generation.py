import random
import string
import math
from ..data.game_constants import (
    CITY_SPACING, CITY_SIZE, MIN_BUILDINGS_PER_CITY, MAX_BUILDINGS_PER_CITY,
    MIN_BUILDING_DIM, MAX_BUILDING_DIM, ROAD_WIDTH, BUILDING_SHOP_BUFFER
)
from ..data.cosmetics import BUILDING_NAME_CHARS
from ..data.buildings import BUILDING_DATA
from ..data.shops import SHOP_DATA
from ..data.terrain import TERRAIN_DATA
from ..data.factions import FACTION_DATA

building_cache = {}

def get_city_faction(x, y):
    """Determines the faction for a given world coordinate."""
    closest_faction = None
    min_dist = float('inf')
    for faction_id, faction_info in FACTION_DATA.items():
        hub_x, hub_y = faction_info["hub_city_coordinates"]
        dist = math.sqrt((x - hub_x * CITY_SPACING)**2 + (y - hub_y * CITY_SPACING)**2)
        if dist < min_dist:
            min_dist = dist
            closest_faction = faction_id
    return closest_faction

def get_city_name(grid_x, grid_y):
    """Generates a city name based on grid coordinates."""
    for faction_id, faction_info in FACTION_DATA.items():
        if (grid_x, grid_y) == faction_info["hub_city_coordinates"]:
            return faction_info["name"]

    name = ""
    index = abs(grid_x * 31 + grid_y * 17 + (grid_x ^ grid_y))
    if index == 0: return "City Prime"
    alphabet = string.ascii_uppercase
    base = len(alphabet)
    while index > 0:
        index, rem = divmod(index - 1, base)
        name = alphabet[rem] + name
    return f"City {name}"

def generate_building_name(local_random, max_width_chars):
    """Generates a short random name for a generic building."""
    name_len = local_random.randint(max(1, max_width_chars - 4), max_width_chars - 1)
    name = "".join(local_random.choice(BUILDING_NAME_CHARS) for _ in range(name_len))
    return name

def generate_city(grid_x, grid_y):
    """Deterministically generates building rectangles for a given city grid."""
    cache_key = (grid_x, grid_y)
    if cache_key in building_cache:
        return building_cache[cache_key]

    buildings = []
    occupied_zones = []
    city_seed = f"{grid_x}-{grid_y}"
    local_random = random.Random(city_seed)
    
    required_buildings = ["mechanic_shop", "gas_station", "weapon_shop", "city_hall"]
    
    city_start_x = grid_x * CITY_SPACING - CITY_SIZE // 2
    city_start_y = grid_y * CITY_SPACING - CITY_SIZE // 2

    for building_type in required_buildings:
        building_info = BUILDING_DATA[building_type]
        b_w, b_h = building_info["width"], building_info["height"]
        
        for _ in range(50): # More attempts for required buildings
            margin = ROAD_WIDTH // 2 + 2
            b_x = local_random.randint(city_start_x + margin, city_start_x + CITY_SIZE - b_w - margin)
            b_y = local_random.randint(city_start_y + margin, city_start_y + CITY_SIZE - b_h - margin)
            
            new_building = {"x": b_x, "y": b_y, "w": b_w, "h": b_h}
            
            overlaps = False
            for existing_b in occupied_zones:
                if (new_building["x"] < existing_b["x"] + existing_b["w"] + BUILDING_SHOP_BUFFER and
                    new_building["x"] + new_building["w"] + BUILDING_SHOP_BUFFER > existing_b["x"] and
                    new_building["y"] < existing_b["y"] + existing_b["h"] + BUILDING_SHOP_BUFFER and
                    new_building["y"] + new_building["h"] + BUILDING_SHOP_BUFFER > existing_b["y"]):
                    overlaps = True
                    break
            
            if not overlaps:
                building_data = {**new_building, "type": building_type, "city_id": cache_key}
                buildings.append(building_data)
                occupied_zones.append(new_building)
                break

    num_generic_buildings = local_random.randint(MIN_BUILDINGS_PER_CITY, MAX_BUILDINGS_PER_CITY)
    for _ in range(num_generic_buildings):
        b_w = local_random.randint(MIN_BUILDING_DIM, MAX_BUILDING_DIM)
        b_h = local_random.randint(MIN_BUILDING_DIM, MAX_BUILDING_DIM)
        
        for _ in range(20): # Placement attempts
            margin = ROAD_WIDTH // 2 + 2
            b_x = local_random.randint(city_start_x + margin, city_start_x + CITY_SIZE - b_w - margin)
            b_y = local_random.randint(city_start_y + margin, city_start_y + CITY_SIZE - b_h - margin)
            
            new_building = {"x": b_x, "y": b_y, "w": b_w, "h": b_h}
            
            overlaps = False
            for existing_b in occupied_zones:
                if (new_building["x"] < existing_b["x"] + existing_b["w"] + 2 and
                    new_building["x"] + new_building["w"] + 2 > existing_b["x"] and
                    new_building["y"] < existing_b["y"] + existing_b["h"] + 2 and
                    new_building["y"] + new_building["h"] + 2 > existing_b["y"]):
                    overlaps = True
                    break
            
            if not overlaps:
                building_name = generate_building_name(local_random, b_w)
                building_data = {**new_building, "type": "GENERIC", "name": building_name, "city_id": cache_key}
                buildings.append(building_data)
                occupied_zones.append(new_building)
                break

    building_cache[cache_key] = buildings
    return buildings

def get_buildings_in_city(grid_x, grid_y):
    """Gets the buildings for a city, generating them if not cached."""
    cache_key = (grid_x, grid_y)
    if cache_key not in building_cache:
        building_cache[cache_key] = generate_city(grid_x, grid_y)
    return building_cache[cache_key]
