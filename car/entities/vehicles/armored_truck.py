from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class ArmoredTruck(Vehicle):
    """
    A heavily armored security truck. Slow but incredibly durable.
    Its AI is simple and direct: close the distance and crush the target.
    """
    def __init__(self, x, y):
        # 8-directional art for a Brinks-style armored truck
        art = {
            # North (Facing Up) - cab at top, heavy boxy body
            "N": [
                "  ▄▓▓▓▄  ",
                " ▟▒▒▒▒▒▙ ",
                "●█▒▒▒▒▒█●",
                "█████████",
                "●███████●",
                " ▀█████▀ "
            ],
            # South (Facing Down) - cab at bottom
            "S": [
                " ▄█████▄ ",
                "●███████●",
                "█████████",
                "●█▒▒▒▒▒█●",
                " ▜▒▒▒▒▒▛ ",
                "  ▀▓▓▓▀  "
            ],
            # East (Facing Right) - cab on right
            "E": [
                "●▓██████▒▒▓▄ ",
                "████████▒▒▒▒▌",
                "████████▒▒▒▒▌",
                "●▓██████▒▒▓▀ "
            ],
            # West (Facing Left) - cab on left
            "W": [
                " ▄▓▒▒██████▓●",
                "▐▒▒▒▒████████",
                "▐▒▒▒▒████████",
                " ▀▓▒▒██████▓●"
            ],
            # North-East - front at upper-right
            "NE": [
                "   ▄▄▒▒▓▄",
                "  ●█▒▒▒▒█",
                " ▐██████●",
                "▐████████",
                " ▀██████▀"
            ],
            # North-West - front at upper-left (mirror NE)
            "NW": [
                "▄▓▒▒▄▄   ",
                "█▒▒▒▒█●  ",
                "●██████▌ ",
                "████████▌",
                "▀██████▀ "
            ],
            # South-East - front at lower-right
            "SE": [
                " ▄██████▄",
                "▐████████",
                " ▐██████●",
                "  ●█▒▒▒▒█",
                "   ▀▀▒▒▓▀"
            ],
            # South-West - front at lower-left (mirror SE)
            "SW": [
                "▄██████▄ ",
                "████████▌",
                "●██████▌ ",
                "█▒▒▒▒█●  ",
                "▀▓▒▒▀▀   "
            ]
        }
        # Upgraded stats to match its appearance
        super().__init__(x, y, art, durability=250, speed=2.7 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.2, handling=0.05)
        self.name = "Armored Truck"
        self.xp_value = 50
        self.cash_value = 100
        self.drop_item = "repair_kit"
        self.drop_rate = 0.5
        self.collision_damage = 12
        self.shoot_damage = 4

        # More aggressive AI phases
        self.phases = [
            {"name": "Chase", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"Shoot": 0.6, "PrepareRam": 0.4}},
            {"name": "Shoot", "duration": (3, 5), "behavior": "SHOOT", "next_phases": {"PrepareRam": 1.0}},
            {"name": "PrepareRam", "duration": (1, 2), "behavior": "EVADE", "next_phases": {"Ram": 1.0}},
            {"name": "Ram", "duration": (3, 4), "behavior": "RAM", "next_phases": {"Chase": 1.0}},
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        """Draws the vehicle on the screen."""
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
