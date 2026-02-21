from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class MuscleCar(Vehicle):
    """
    A classic, high-performance muscle car. It's fast, aggressive,
    and built for high-speed combat.
    """
    def __init__(self, x, y):
        # Art inspired by the iconic Fast & Furious muscle car
        art = {
            # North (Facing Up) - hood at top, trunk at bottom
            "N": [
                "  ▄▓▓▄  ",
                " ▓░░░░▓ ",
                "●█▓▓▓▓█●",
                "█▓████▓█",
                "●██████●",
                " ▀▀██▀▀ "
            ],
            # South (Facing Down) - vertical mirror of N
            "S": [
                " ▄▄██▄▄ ",
                "●██████●",
                "█▓████▓█",
                "●█▓▓▓▓█●",
                " ▓░░░░▓ ",
                "  ▀▓▓▀  "
            ],
            # East (Facing Right) - hood on right, wide stance
            "E": [
                "●▓████░░▓▄  ",
                "██▓████▓░░▓▌",
                "●▓████░░▓▀  "
            ],
            # West (Facing Left) - horizontal mirror of E
            "W": [
                "  ▄▓░░████▓●",
                "▐▓░░▓████▓██",
                "  ▀▓░░████▓●"
            ],
            # North-East - front at upper-right
            "NE": [
                "   ▄▄░▓▓▄",
                "  ●█░░▓▓█",
                " █▓▓▓███●",
                "▐█▓████▀ ",
                " ▀███▀   "
            ],
            # North-West - horizontal mirror of NE
            "NW": [
                "▄▓▓░▄▄   ",
                "█▓▓░░█●  ",
                "●███▓▓▓█ ",
                " ▀████▓█▌",
                "   ▀███▀ "
            ],
            # South-East - vertical mirror of NE
            "SE": [
                " ▄███▄   ",
                "▐█▓████▄ ",
                " █▓▓▓███●",
                "  ●█░░▓▓█",
                "   ▀▀░▓▓▀"
            ],
            # South-West - horizontal mirror of SE
            "SW": [
                "   ▄███▄ ",
                " ▄████▓█▌",
                "●███▓▓▓█ ",
                "█▓▓░░█●  ",
                "▀▓▓░▀▀   "
            ]
        }
        super().__init__(x, y, art, durability=85, speed=10.1 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.9, handling=0.18, weight=1500)
        self.name = "Muscle Car"
        self.xp_value = 40
        self.cash_value = 75
        self.drop_item = "repair_kit"
        self.drop_rate = 0.1
        self.collision_damage = 8
        self.shoot_damage = 4

        # Aggressive, multi-phase AI for a skilled driver
        self.phases = [
            {"name": "AggressiveChase", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"StrafeAndShoot": 1.0}},
            {"name": "StrafeAndShoot", "duration": (3, 5), "behavior": "SHOOT", "next_phases": {"Flank": 0.5, "RammingRun": 0.5}},
            {"name": "Flank", "duration": (3, 4), "behavior": "FLANK", "next_phases": {"AggressiveChase": 0.7, "StrafeAndShoot": 0.3}},
            {"name": "RammingRun", "duration": (2, 3), "behavior": "RAM", "next_phases": {"AggressiveChase": 1.0}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        """Draws the vehicle on the screen."""
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
