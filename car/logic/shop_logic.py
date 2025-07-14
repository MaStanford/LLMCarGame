import curses
from .shop import Shop
from ..data.buildings import BUILDING_DATA
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city, get_city_faction
from .inventory_generation import generate_inventory
from ..ui.shop import draw_shop_menu

from .collision_detection import find_safe_exit_spot
