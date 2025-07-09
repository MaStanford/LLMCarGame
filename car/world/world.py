import random
import math
from .generation import get_buildings_in_city
from ..data import TERRAIN_DATA, CITY_SPACING, ROAD_WIDTH

class World:
    def __init__(self, seed):
        self.seed = seed
        self.random = random.Random(seed)
        self.chunks = {}

    def get_chunk(self, chunk_x, chunk_y):
        if (chunk_x, chunk_y) not in self.chunks:
            self.generate_chunk(chunk_x, chunk_y)
        return self.chunks[(chunk_x, chunk_y)]

    def generate_chunk(self, chunk_x, chunk_y):
        chunk_size = 32
        chunk = []
        for y in range(chunk_size):
            row = []
            for x in range(chunk_size):
                world_x = chunk_x * chunk_size + x
                world_y = chunk_y * chunk_size + y
                terrain = self.get_terrain_at(world_x, world_y)
                row.append(terrain)
            chunk.append(row)
        self.chunks[(chunk_x, chunk_y)] = chunk

    def get_terrain_at(self, x, y):
        # Check for roads
        if abs(x % CITY_SPACING) < ROAD_WIDTH / 2 or abs(y % CITY_SPACING) < ROAD_WIDTH / 2:
            return TERRAIN_DATA["asphalt"]

        # Check for cities
        grid_x = round(x / CITY_SPACING)
        grid_y = round(y / CITY_SPACING)
        city_buildings = get_buildings_in_city(grid_x, grid_y)
        for building in city_buildings:
            if building['x'] <= x < building['x'] + building['w'] and \
               building['y'] <= y < building['y'] + building['h']:
                return TERRAIN_DATA["concrete"]

        # Default to wilderness
        return TERRAIN_DATA["grass"]

