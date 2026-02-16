from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class WarRig(Vehicle):
    """
    The formidable command vehicle of the Dustwind Caravans.
    It's slow but heavily armored, lays mines, and can defend itself.
    """
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - cab at top, massive trailer body
            "N": [
                "  ▄▓▓▓▄  ",
                " ◢░░░░░◣ ",
                "●▒░░░░░▒●",
                "█████████",
                "●███████●",
                "█████████",
                "█████████",
                "●███████●",
                " ▀█████▀ "
            ],
            # South (Facing Down) - cab at bottom
            "S": [
                " ▄█████▄ ",
                "●███████●",
                "█████████",
                "█████████",
                "●███████●",
                "█████████",
                "●▒░░░░░▒●",
                " ◥░░░░░◤ ",
                "  ▀▓▓▓▀  "
            ],
            # East (Facing Right) - cab on right, long trailer
            "E": [
                "●▓████████████░░▓▄ ",
                "██████████████░░░░▌",
                "●▓█████●▓████░░░░▌",
                "●▓████████████░░▓▀ "
            ],
            # West (Facing Left) - cab on left, long trailer
            "W": [
                " ▄▓░░████████████▓●",
                "▐░░░░██████████████",
                "▐░░░░████▓●█████▓●",
                " ▀▓░░████████████▓●"
            ],
            # North-East - front at upper-right
            "NE": [
                "    ▄▄░░▓▄",
                "   ●█░░░░█",
                "  ▐██████●",
                " ▐████████",
                "▐█████████",
                " ●████████",
                "  ▀██████▀"
            ],
            # North-West - front at upper-left (mirror NE)
            "NW": [
                "▄▓░░▄▄    ",
                "█░░░░█●   ",
                "●██████▌  ",
                "████████▌ ",
                "█████████▌",
                "████████● ",
                "▀██████▀  "
            ],
            # South-East - front at lower-right
            "SE": [
                "  ▄██████▄",
                " ●████████",
                "▐█████████",
                " ▐████████",
                "  ▐██████●",
                "   ●█░░░░█",
                "    ▀▀░░▓▀"
            ],
            # South-West - front at lower-left (mirror SE)
            "SW": [
                "▄██████▄  ",
                "████████● ",
                "█████████▌",
                "████████▌ ",
                "●██████▌  ",
                "█░░░░█●   ",
                "▀▓░░▀▀    "
            ]
        }
        super().__init__(x, y, art, durability=300, speed=3.0 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.2, handling=0.03)
        self.name = "War Rig"
        self.xp_value = 200
        self.cash_value = 300
        self.drop_item = "repair_kit"
        self.drop_rate = 1.0  # Always drops a repair kit
        self.collision_damage = 15
        self.shoot_damage = 5
        self.phases = [
            {"name": "Advance", "duration": (8, 10), "behavior": "CHASE", "next_phases": {"Shoot": 0.6, "DeployMines": 0.4}},
            {"name": "Shoot", "duration": (4, 6), "behavior": "SHOOT", "next_phases": {"DeployMines": 0.5, "Advance": 0.5}},
            {"name": "DeployMines", "duration": (2, 3), "behavior": "DEPLOY_MINE", "next_phases": {"Advance": 1.0}},
            {"name": "Evade", "duration": (4, 5), "behavior": "EVADE", "next_phases": {"Advance": 1.0}}
        ]
        self._initialize_ai()

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_DUSTWIND", 0), transparent_bg=True)
