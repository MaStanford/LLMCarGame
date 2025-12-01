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

building_cache = {}

def _get_neutral_faction_id(faction_data):
    """Finds the ID of the neutral faction."""
    for faction_id, data in faction_data.items():
        if data.get("hub_city_coordinates") == [0, 0]:
            return faction_id
    return None # Fallback

def get_city_faction(x, y, faction_data):
    """Determines the faction for a given world coordinate."""
    grid_x = round(x / CITY_SPACING)
    grid_y = round(y / CITY_SPACING)

    # The central city is always the neutral hub
    if grid_x == 0 and grid_y == 0:
        return _get_neutral_faction_id(faction_data)

    closest_faction = None
    min_dist = float('inf')
    for faction_id, faction_info in faction_data.items():
        hub_x, hub_y = faction_info["hub_city_coordinates"]
        dist = math.sqrt((grid_x - hub_x)**2 + (grid_y - hub_y)**2)
        if dist < min_dist:
            min_dist = dist
            closest_faction = faction_id
    return closest_faction

def get_city_name(grid_x, grid_y, faction_data):
    """Generates a consistent name for a city at the given grid coordinates."""
    # Check if it's a hub city
    for faction_id, data in faction_data.items():
        hub_coords = data.get("hub_city_coordinates")
        if hub_coords:
            hub_x, hub_y = hub_coords
            # Coordinates in faction_data are world coords, compare with grid coords * spacing
            if hub_x == grid_x * CITY_SPACING and hub_y == grid_y * CITY_SPACING:
                 return f"{data['name']} Hub"

    # Procedural name for non-hub cities
    local_random = random.Random(f"city_name_{grid_x}_{grid_y}")
    prefixes = ["New", "Old", "Fort", "Mount", "Lake", "Iron", "Rust", "Dust", "Scrap"]
    suffixes = ["ton", "ville", "burg", "haven", " City", " Outpost", " Junction"]
    
    return f"{local_random.choice(prefixes)}{local_random.choice(suffixes)}"

def does_city_exist_at(grid_x, grid_y, seed, factions):
    """Deterministically checks if a city exists at a given grid coordinate."""
    # Hub cities always exist
    for faction in factions.values():
        if faction.get("hub_city_coordinates") == [grid_x, grid_y]:
            return True
        
    # Use a deterministic random number generator based on the world seed and coordinates
    local_random = random.Random(f"{seed}-{grid_x}-{grid_y}")
    
    # Adjust probability based on distance from the center (0,0)
    distance = math.sqrt(grid_x**2 + grid_y**2)
    probability = max(0.1, 0.8 - distance * 0.02) # Decrease probability farther out
    
    return local_random.random() < probability

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
                # This is the key fix: the 'type' used for interaction checks
                # should be the building's key, e.g., "mechanic_shop".
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

def find_safe_spawn_point(start_x, start_y, buildings, player_car, max_radius=20):
    """
    Finds a safe spawn point near a building, ensuring the entire player vehicle
    area (plus a buffer) is clear of other buildings.
    """
    car_w = player_car.width + 2  # Add a 1-char buffer on each side
    car_h = player_car.height + 2 # Add a 1-char buffer on each side

    for r in range(1, max_radius + 1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if abs(dx) + abs(dy) != r: continue

                check_x = start_x + dx
                check_y = start_y + dy
                
                # Define the bounding box of the potential spawn area
                spawn_box = {
                    "x": check_x - car_w / 2, "y": check_y - car_h / 2,
                    "w": car_w, "h": car_h
                }

                is_safe = True
                for building in buildings:
                    # Simple AABB collision check
                    if (spawn_box["x"] < building["x"] + building["w"] and
                        spawn_box["x"] + spawn_box["w"] > building["x"] and
                        spawn_box["y"] < building["y"] + building["h"] and
                        spawn_box["y"] + spawn_box["h"] > building["y"]):
                        is_safe = False
                        break
                
                if is_safe:
                    return check_x, check_y
    
    return start_x, start_y + 2
