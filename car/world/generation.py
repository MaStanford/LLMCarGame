import random
import string
from ..data.game_constants import (
    CITY_SPACING, CITY_SIZE, MIN_BUILDINGS_PER_CITY, MAX_BUILDINGS_PER_CITY,
    MIN_BUILDING_DIM, MAX_BUILDING_DIM, ROAD_WIDTH, BUILDING_SHOP_BUFFER
)
from ..data.cosmetics import BUILDING_NAME_CHARS
from ..data.buildings import BUILDING_DATA
from ..data.shops import SHOP_DATA
from ..data.terrain import TERRAIN_DATA

# Cache for building layouts to avoid regenerating every frame
building_cache = {}

def get_city_name(grid_x, grid_y):
    """Generates a city name based on grid coordinates."""
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
    name_len = local_random.randint(max(1, max_width_chars - 4), max_width_chars - 1) # Ensure it fits
    name = "".join(local_random.choice(BUILDING_NAME_CHARS) for _ in range(name_len))
    return name

def get_buildings_in_city(grid_x, grid_y):
    """Deterministically generates building rectangles for a given city grid."""
    cache_key = (grid_x, grid_y)
    if cache_key in building_cache:
        return building_cache[cache_key]

    buildings = []
    city_seed = f"{grid_x}-{grid_y}"
    local_random = random.Random(city_seed)
    
    required_buildings = ["mechanic_shop", "gas_station", "weapon_shop", "city_hall"]
    
    city_start_x = grid_x * CITY_SPACING - CITY_SIZE // 2
    city_start_y = grid_y * CITY_SPACING - CITY_SIZE // 2

    # --- Place Required Buildings ---
    for building_type in required_buildings:
        building_info = BUILDING_DATA[building_type]; b_w = building_info["width"]; b_h = building_info["height"]
        placed = False
        for _ in range(20): # More attempts to ensure placement
            margin = ROAD_WIDTH // 2 + 2
            min_bx = city_start_x + margin; max_bx = city_start_x + CITY_SIZE - b_w - margin
            min_by = city_start_y + margin; max_by = city_start_y + CITY_SIZE - b_h - margin
            if min_bx > max_bx or min_by > max_by: continue
            b_x = local_random.randint(min_bx, max_bx); b_y = local_random.randint(min_by, max_by)
            
            road_clearance = ROAD_WIDTH / 2 + max(b_w, b_h) / 2 + 2
            on_horiz_road_center = abs(b_y + b_h/2 - (grid_y * CITY_SPACING)) < road_clearance
            on_vert_road_center = abs(b_x + b_w/2 - (grid_x * CITY_SPACING)) < road_clearance
            
            overlaps = False
            for existing_b in buildings:
                buffer = BUILDING_SHOP_BUFFER
                if (b_x < existing_b["x"] + existing_b["w"] + buffer and
                    b_x + b_w + buffer > existing_b["x"] and
                    b_y < existing_b["y"] + existing_b["h"] + buffer and
                    b_y + b_h + buffer > existing_b["y"]):
                    overlaps = True; break
            
            if not (on_horiz_road_center or on_vert_road_center) and not overlaps:
                buildings.append({"x": b_x, "y": b_y, "w": b_w, "h": b_h, "type": building_type})
                placed = True; break

    # --- Place Generic Buildings ---
    num_generic_buildings = local_random.randint(MIN_BUILDINGS_PER_CITY - len(required_buildings), MAX_BUILDINGS_PER_CITY - len(required_buildings))
    for _ in range(num_generic_buildings):
        b_w = local_random.randint(MIN_BUILDING_DIM, MAX_BUILDING_DIM)
        b_h = local_random.randint(MIN_BUILDING_DIM, MAX_BUILDING_DIM)
        placed = False
        for _ in range(10): # Placement attempts
            margin = ROAD_WIDTH // 2 + 2
            min_bx = city_start_x + margin; max_bx = city_start_x + CITY_SIZE - b_w - margin
            min_by = city_start_y + margin; max_by = city_start_y + CITY_SIZE - b_h - margin
            if min_bx > max_bx or min_by > max_by: continue
            b_x = local_random.randint(min_bx, max_bx); b_y = local_random.randint(min_by, max_by)
            
            road_clearance = ROAD_WIDTH / 2 + max(b_w, b_h) / 2 + 2
            on_horiz_road_center = abs(b_y + b_h/2 - (grid_y * CITY_SPACING)) < road_clearance
            on_vert_road_center = abs(b_x + b_w/2 - (grid_x * CITY_SPACING)) < road_clearance
            
            overlaps = False
            for existing_b in buildings:
                buffer = BUILDING_SHOP_BUFFER if existing_b.get("type") in SHOP_DATA else 2
                if (b_x < existing_b["x"] + existing_b["w"] + buffer and
                    b_x + b_w + buffer > existing_b["x"] and
                    b_y < existing_b["y"] + existing_b["h"] + buffer and
                    b_y + b_h + buffer > existing_b["y"]):
                    overlaps = True; break
            
            if not (on_horiz_road_center or on_vert_road_center) and not overlaps:
                building_name = generate_building_name(local_random, b_w)
                buildings.append({"x": b_x, "y": b_y, "w": b_w, "h": b_h, "type": "GENERIC", "name": building_name})
                placed = True; break

    building_cache[cache_key] = buildings
    return buildings
