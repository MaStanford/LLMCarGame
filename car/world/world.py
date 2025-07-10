import random
import math
from .generation import get_buildings_in_city
from ..data.game_constants import CITY_SPACING, ROAD_WIDTH, CITY_SIZE
from ..data.terrain import TERRAIN_DATA

class World:
    def __init__(self, seed):
        self.seed = seed
        self.random = random.Random(seed)

    def get_terrain_at(self, x, y):
        # Check for roads
        if abs(x % CITY_SPACING) < ROAD_WIDTH / 2 or abs(y % CITY_SPACING) < ROAD_WIDTH / 2:
            return TERRAIN_DATA["ROAD"]

        # Check for cities
        grid_x = round(x / CITY_SPACING)
        grid_y = round(y / CITY_SPACING)
        
        # Check if inside a city boundary
        city_center_x = grid_x * CITY_SPACING
        city_center_y = grid_y * CITY_SPACING
        if abs(x - city_center_x) < CITY_SIZE / 2 and abs(y - city_center_y) < CITY_SIZE / 2:
            # Check for buildings within the city
            city_buildings = get_buildings_in_city(grid_x, grid_y)
            for building in city_buildings:
                if building['x'] <= x < building['x'] + building['w'] and \
                   building['y'] <= y < building['y'] + building['h']:
                    return TERRAIN_DATA["BUILDING_WALL"]
            return TERRAIN_DATA["ROAD"] # Asphalt for city ground

        # Default to wilderness
        return TERRAIN_DATA["GRASS"]

