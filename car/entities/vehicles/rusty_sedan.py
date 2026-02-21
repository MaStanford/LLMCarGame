from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class RustySedan(Vehicle):
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - beat-up sedan, dented hood at top
            "N": [
                " ▄░▄ ",
                "●▒░▒●",
                "█░▓░█",
                "●▓█▓●",
                " ▀▓▀ "
            ],
            # South (Facing Down) - trunk at top
            "S": [
                " ▄▓▄ ",
                "●▓█▓●",
                "█░▓░█",
                "●▒░▒●",
                " ▀░▀ "
            ],
            # East (Facing Right) - hood on right, rusty panels
            "E": [
                "●░██▓░▒▄ ",
                "█▒███░▒░▌",
                "●░██▓░▒▀ "
            ],
            # West (Facing Left) - hood on left
            "W": [
                " ▄▒░▓██░●",
                "▐░▒░███▒█",
                " ▀▒░▓██░●"
            ],
            # North-East - front at upper-right
            "NE": [
                "  ▄▒░▒▄",
                " ●█░▒░█",
                "▐█░▓█▓●",
                " ▀▓█▀  "
            ],
            # North-West - front at upper-left (mirror NE)
            "NW": [
                "▄▒░▒▄  ",
                "█░▒░█● ",
                "●▓█░▓█▌",
                "  ▀█▓▀ "
            ],
            # South-East - front at lower-right
            "SE": [
                " ▄█▓▄  ",
                "▐█░▓█▓●",
                " ●█░▒░█",
                "  ▀▒░▒▀"
            ],
            # South-West - front at lower-left (mirror SE)
            "SW": [
                "  ▄▓█▄ ",
                "●▓█░▓█▌",
                "█░▒░█● ",
                "▀▒░▒▀  "
            ]
        }
        super().__init__(x, y, art, durability=20, speed=6.75 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.5, handling=0.5, weight=1000)
        self.name = "Rusty Sedan"
        self.xp_value = 5
        self.cash_value = 10
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.05
        self.collision_damage = 3
        self.shoot_damage = 2
        self.phases = [
            {"name": "Pursuit", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"DriveBy": 1.0}},
            {"name": "DriveBy", "duration": (3, 5), "behavior": "SHOOT", "next_phases": {"Pursuit": 0.5, "Reposition": 0.5}},
            {"name": "Reposition", "duration": (2, 3), "behavior": "EVADE", "next_phases": {"Pursuit": 1.0}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
