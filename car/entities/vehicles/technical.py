from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Technical(Vehicle):
    """
    A versatile, gun-mounted pickup used by the Salvage Core.
    It balances direct pursuit with suppressive fire from a distance.
    """
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - cab at top, gun turret visible on bed
            "N": [
                " ▄▓▓▄ ",
                "●░▒▒░●",
                "█╦▆╦█",
                "█═══█",
                "●███●",
                " ▀█▀ "
            ],
            # South (Facing Down) - cab at bottom, bed with gun at top
            "S": [
                " ▄█▄ ",
                "●███●",
                "█═══█",
                "█╩▆╩█",
                "●░▒▒░●",
                " ▀▓▓▀ "
            ],
            # East (Facing Right) - cab right, gun turret on bed
            "E": [
                "  ╦╗▄▓▓▄ ",
                "●═▆═█▒▒░▌",
                "●═══█▒▒░▌",
                "  ╩╝▀▓▓▀ "
            ],
            # West (Facing Left) - cab left, gun turret on bed
            "W": [
                " ▄▓▓▄╔╦  ",
                "▐░▒▒█═▆═●",
                "▐░▒▒█═══●",
                " ▀▓▓▀╚╩  "
            ],
            # North-East - front at upper-right, turret visible
            "NE": [
                "  ╦▄▓▄",
                " ●▆▒▒█",
                "▐█═▓█●",
                "▐██══▀",
                " ▀██▀ "
            ],
            # North-West - front at upper-left (mirror NE)
            "NW": [
                "▄▓▄╦  ",
                "█▒▒▆● ",
                "●█▓═█▌",
                "▀══██▌",
                " ▀██▀ "
            ],
            # South-East - front at lower-right
            "SE": [
                " ▄██▄ ",
                "▐██══▄",
                "▐█═▓█●",
                " ●▆▒▒█",
                "  ╩▀▓▀"
            ],
            # South-West - front at lower-left (mirror SE)
            "SW": [
                " ▄██▄ ",
                "▄══██▌",
                "●█▓═█▌",
                "█▒▒▆● ",
                "▀▓▀╩  "
            ]
        }
        super().__init__(x, y, art, durability=70, speed=8.25 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.5, handling=0.6, weight=1200)
        self.name = "Technical"
        self.xp_value = 25
        self.cash_value = 40
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.25
        self.collision_damage = 5
        self.shoot_damage = 4
        self.phases = [
            {"name": "Approach", "duration": (3, 5), "behavior": "CHASE", "next_phases": {"SuppressiveFire": 1.0}},
            {"name": "SuppressiveFire", "duration": (4, 6), "behavior": "SHOOT", "next_phases": {"Flank": 0.6, "Approach": 0.4}},
            {"name": "Flank", "duration": (3, 4), "behavior": "FLANK", "next_phases": {"SuppressiveFire": 0.7, "Approach": 0.3}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_SALVAGE", 0), transparent_bg=True)
