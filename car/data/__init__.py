from .fauna import FAUNA_DATA, TOTAL_FAUNA_SPAWN_RATE
from .cars import CARS_DATA
from .colors import COLOR_PAIRS_DEFS
from .game_constants import *
from .experience import *
from .difficulty import DIFFICULTY_LEVELS, DIFFICULTY_MODIFIERS
from .pickups import *
from .terrain import TERRAIN_DATA
from .shops import SHOP_DATA
from .cosmetics import BUILDING_OUTLINE, BUILDING_NAME_CHARS
from .weapons import WEAPONS_DATA
from .obstacles import OBSTACLE_DATA, TOTAL_SPAWN_RATE
from ..common import get_car_dimensions

MAX_CAR_WIDTH_ACROSS_ALL = 0
for car_data in CARS_DATA:
    _, width = get_car_dimensions(car_data["art"])
    MAX_CAR_WIDTH_ACROSS_ALL = max(MAX_CAR_WIDTH_ACROSS_ALL, width)
ROAD_WIDTH = MAX_CAR_WIDTH_ACROSS_ALL + 6 # Make road wider than widest car + padding
