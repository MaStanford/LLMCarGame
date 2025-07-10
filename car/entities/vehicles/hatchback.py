from .player_car import PlayerCar

class Hatchback(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  ____  ",
                " / __ \\ ",
                "| |  | |",
                " \\____/ "
            ],
            "NE": [
                "  __..  ",
                " /  / | ",
                "|__| /  ",
                " `-./`   "
            ],
            "E": [
                "  ____ ",
                " / __`\\",
                "| |__| |",
                " \\____/"
            ],
            "SE": [
                "  ..__  ",
                " |  \\ `\\",
                "  \\__| |",
                "   `\\.-` "
            ],
            "S": [
                "  ____  ",
                " /    \\ ",
                "| |__| |",
                " \\____/ "
            ],
            "SW": [
                "   __.. ",
                "  |   \\ `\\",
                "   \\__| |",
                "    `.-`  "
            ],
            "W": [
                "   ____  ",
                "  / `__\\ ",
                " | |__| |",
                "  \\____/ "
            ],
            "NW": [
                " ..__   ",
                "|   \\ `\\ ",
                "|__|\\/   ",
                " `-`    "
            ]
        }
        super().__init__(
            x, y, art,
            durability=90,
            speed=8.0,
            acceleration=0.7,
            handling=0.12,
            braking_power=0.75,
            attachment_points={
                "hood_gun": {"level": "light", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"level": "light", "offset_x": 0, "offset_y": -1},
                "hatch_gun": {"level": "medium", "offset_x": 0, "offset_y": 2}
            }
        )
        self.default_weapons = {
            "hatch_gun": "wep_shotgun"
        }
