from ..vehicle import Vehicle
from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class RaiderBuggy(Vehicle):
    """
    A fast, aggressive buggy used by the Crimson Cartel.
    It harasses from a distance before closing in for a ramming attack.
    """
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - aggressive front wedge at top
            "N": [
                " ▄▲▄ ",
                "▗░▓░▖",
                "●-█-●",
                " ▀ ▀ "
            ],
            # South (Facing Down) - rear at top
            "S": [
                " ▄ ▄ ",
                "●-█-●",
                "▝░▓░▘",
                " ▀▼▀ "
            ],
            # East (Facing Right) - front on right
            "E": [
                "●░░-▲▄",
                "█▓█-█░▌",
                "●░░-▼▀"
            ],
            # West (Facing Left) - front on left
            "W": [
                "▄▲-░░●",
                "▐░█-█▓█",
                "▀▼-░░●"
            ],
            # North-East - front at upper-right
            "NE": [
                "  ▄░▲",
                " ●▓█░",
                "▗█▓█●",
                " ▀▀  "
            ],
            # North-West - front at upper-left (mirror NE)
            "NW": [
                "▲░▄  ",
                "░█▓● ",
                "●█▓█▖",
                "  ▀▀ "
            ],
            # South-East - front at lower-right (mirror NE vertically)
            "SE": [
                " ▄▄  ",
                "▗█▓█●",
                " ●▓█░",
                "  ▀░▼"
            ],
            # South-West - front at lower-left (mirror SE)
            "SW": [
                "  ▄▄ ",
                "●█▓█▖",
                "░█▓● ",
                "▼░▀  "
            ]
        }
        super().__init__(x, y, art, durability=40, speed=9.0 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.7, handling=0.8, weight=600)
        self.name = "Raider Buggy"
        self.xp_value = 15
        self.cash_value = 20
        self.collision_damage = 5
        self.shoot_damage = 3
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.15
        self.phases = [
            {"name": "Harass", "duration": (3, 5), "behavior": "STRAFE", "next_phases": {"Shoot": 0.5, "Ram": 0.5}},
            {"name": "Shoot", "duration": (2, 4), "behavior": "SHOOT", "next_phases": {"Harass": 0.6, "Ram": 0.4}},
            {"name": "Ram", "duration": (2, 3), "behavior": "RAM", "next_phases": {"Harass": 1.0}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_CRIMSON", 0), transparent_bg=True)
