from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Miner(Vehicle):
    """
    A heavy, armored vehicle that lays mines.
    """
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - hood at top, mine payload in center
            "N": [
                " ▄█▄ ",
                "●▒▒▒●",
                "█▒▒▒█",
                "●▓▓▓●",
                " ▀█▀ "
            ],
            # South (Facing Down) - vertical mirror of N
            "S": [
                " ▄█▄ ",
                "●▓▓▓●",
                "█▒▒▒█",
                "●▒▒▒●",
                " ▀█▀ "
            ],
            # East (Facing Right) - mine payload visible
            "E": [
                "●█▒▒▓█▄ ",
                "█▓▒▒▓▒░▌",
                "●█▒▒▓█▀ "
            ],
            # West (Facing Left) - horizontal mirror of E
            "W": [
                " ▄█▓▒▒█●",
                "▐░▒▓▒▒▓█",
                " ▀█▓▒▒█●"
            ],
            # North-East - front at upper-right
            "NE": [
                "  ▄░█▄",
                " ●▒▒▓█",
                "▐█▒▓█●",
                " ▀█▀  "
            ],
            # North-West - horizontal mirror of NE
            "NW": [
                "▄█░▄  ",
                "█▓▒▒● ",
                "●█▓▒█▌",
                "  ▀█▀ "
            ],
            # South-East - vertical mirror of NE
            "SE": [
                " ▄█▄  ",
                "▐█▒▓█●",
                " ●▒▒▓█",
                "  ▀░█▀"
            ],
            # South-West - horizontal mirror of SE
            "SW": [
                "  ▄█▄ ",
                "●█▓▒█▌",
                "█▓▒▒● ",
                "▀█░▀  "
            ]
        }
        super().__init__(x, y, art, durability=150, speed=2.85 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.3, handling=0.05)
        self.name = "Miner"
        self.collision_damage = 10
        self.shoot_damage = 0
        self.xp_value = 60
        self.cash_value = 80
        self.drop_item = "mine"
        self.drop_rate = 0.4
        self.phases = [
            {"name": "Advance", "duration": (5, 8), "behavior": "CHASE", "next_phases": {"DeployMines": 1.0}},
            {"name": "DeployMines", "duration": (2, 3), "behavior": "DEPLOY_MINE", "next_phases": {"Evade": 0.5, "Advance": 0.5}},
            {"name": "Evade", "duration": (3, 4), "behavior": "EVADE", "next_phases": {"Advance": 1.0}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
