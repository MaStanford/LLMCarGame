import random
import string
from ..data import (
    CITY_SPACING, CITY_SIZE, MIN_BUILDINGS_PER_CITY, MAX_BUILDINGS_PER_CITY,
    MIN_BUILDING_DIM, MAX_BUILDING_DIM, ROAD_WIDTH, SHOP_DATA, BUILDING_SHOP_BUFFER,
    TERRAIN_DATA, BUILDING_NAME_CHARS
)

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
    num_buildings = local_random.randint(MIN_BUILDINGS_PER_CITY, MAX_BUILDINGS_PER_CITY)
    shop_types = list(SHOP_DATA.keys())
    city_start_x = grid_x * CITY_SPACING - CITY_SIZE // 2
    city_start_y = grid_y * CITY_SPACING - CITY_SIZE // 2
    placed_shop_types = set()
    shop_attempts = 0
    max_shop_attempts = len(shop_types) * 5

    # --- Place Shops First ---
    while len(placed_shop_types) < len(shop_types) and shop_attempts < max_shop_attempts:
        shop_type = local_random.choice(shop_types)
        if shop_type in placed_shop_types:
            shop_attempts += 1; continue
        shop_info = SHOP_DATA[shop_type]; b_w = shop_info["width"]; b_h = shop_info["height"]
        placed = False
        for _ in range(10): # Placement attempts for this shop
            margin = ROAD_WIDTH // 2 + 2
            min_bx = city_start_x + margin; max_bx = city_start_x + CITY_SIZE - b_w - margin
            min_by = city_start_y + margin; max_by = city_start_y + CITY_SIZE - b_h - margin
            if min_bx > max_bx or min_by > max_by: continue # City too small for this shop + margins
            b_x = local_random.randint(min_bx, max_bx); b_y = local_random.randint(min_by, max_by)
            road_clearance = ROAD_WIDTH / 2 + max(b_w, b_h) / 2 + 2
            on_horiz_road_center = abs(b_y + b_h/2 - (grid_y * CITY_SPACING)) < road_clearance
            on_vert_road_center = abs(b_x + b_w/2 - (grid_x * CITY_SPACING)) < road_clearance
            overlaps = False
            for existing_b in buildings:
                buffer = BUILDING_SHOP_BUFFER # Use defined buffer
                if (b_x < existing_b["x"] + existing_b["w"] + buffer and
                    b_x + b_w + buffer > existing_b["x"] and
                    b_y < existing_b["y"] + existing_b["h"] + buffer and
                    b_y + b_h + buffer > existing_b["y"]):
                    overlaps = True; break
            if not (on_horiz_road_center or on_vert_road_center) and not overlaps:
                buildings.append({"x": b_x, "y": b_y, "w": b_w, "h": b_h, "type": shop_type})
                placed_shop_types.add(shop_type); placed = True; break
        shop_attempts += 1

    # --- Place Generic Buildings ---
    remaining_buildings = num_buildings - len(buildings)
    for _ in range(remaining_buildings):
        b_w = local_random.randint(MIN_BUILDING_DIM, MAX_BUILDING_DIM)
        b_h = local_random.randint(MIN_BUILDING_DIM, MAX_BUILDING_DIM)
        placed = False
        for _ in range(10): # Placement attempts for this generic building
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
                # Use larger buffer when checking against shops for generic buildings
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
