from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class RustBucket(Vehicle):
    """
    A volatile, ram-focused vehicle of the Rust Prophets.
    Its only goal is to collide with the player. Explodes on death.
    """
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - hood at top, O=good headlight (left), X=broken (right)
            "N": [
                " ▄▓▄ ",
                "O░░░X",
                "█▒▓▒█",
                "●█▒█●",
                " ▀█▀ "
            ],
            # South (Facing Down) - vertical mirror of N, X now on left viewed from behind
            "S": [
                " ▄█▄ ",
                "●█▒█●",
                "█▒▓▒█",
                "X░░░O",
                " ▀▓▀ "
            ],
            # East (Facing Right) - O=front-left (top), X=front-right (bottom)
            "E": [
                "●▒██░▓▄O",
                "█▒██▓░░▌",
                "●▒██░▓▀X"
            ],
            # West (Facing Left) - horizontal mirror of E
            "W": [
                "X▄▓░██▒●",
                "▐░░▓██▒█",
                "O▀▓░██▒●"
            ],
            # North-East - front at upper-right, X on outer edge
            "NE": [
                "  ▄░▓▄X",
                " O█░░▓█",
                "▐█▒▓██●",
                " ▀██▀  "
            ],
            # North-West - horizontal mirror of NE, X on outer edge
            "NW": [
                "X▄▓░▄  ",
                "█▓░░█O ",
                "●██▓▒█▌",
                "  ▀██▀ "
            ],
            # South-East - vertical mirror of NE
            "SE": [
                " ▄██▄  ",
                "▐█▒▓██●",
                " O█░░▓█",
                "  ▀░▓▀X"
            ],
            # South-West - horizontal mirror of SE
            "SW": [
                "  ▄██▄ ",
                "●██▓▒█▌",
                "█▓░░█O ",
                "X▀▓░▀  "
            ]
        }
        super().__init__(x, y, art, durability=45, speed=9.3 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.4, handling=0.08)
        self.name = "Rust Bucket"
        self.xp_value = 20
        self.cash_value = 15
        self.collision_damage = 15
        self.shoot_damage = 0
        self.phases = [
            {"name": "Kamikaze", "duration": (10, 10), "behavior": "RAM", "next_phases": {"Kamikaze": 1.0}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        """Draws the vehicle on the screen."""
        from ...rendering.draw_utils import draw_sprite
        # Note the custom color pair for this faction
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_RUST", 0), transparent_bg=True)
