import curses
from ..ui.city_hall import draw_city_hall_menu, draw_quest_briefing
from ..ui.dialog import draw_dialog_modal
from ..data.city_info import CITY_INFO
from .quests import QUEST_TEMPLATES
from ..data.factions import FACTION_DATA
from ..world.generation import get_city_faction
import random

from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city
from ..data.buildings import BUILDING_DATA

from .collision_detection import find_safe_exit_spot

