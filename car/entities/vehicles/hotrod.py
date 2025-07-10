from .player_car import PlayerCar

class Hotrod(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "    ____    ",
                " __/ __ \\__ ",
                "|  |  |  |  |",
                "|__|__|__|__|"
            ],
            "NE": [
                "      __..  ",
                "   __/  /  | ",
                "  |___|  /  ",
                "   `-|_/`   "
            ],
            "E": [
                "   ____    ",
                "  / __ \\__ ",
                " | |__| |__)",
                "  \\____/   "
            ],
            "SE": [
                "  ..__      ",
                " |  \\  \\__  ",
                "  \\  |___|  ",
                "   `\\_|-`   "
            ],
            "S": [
                "    ____    ",
                " __/    \\__ ",
                "|  |____|  |",
                "|__|____|__|"
            ],
            "SW": [
                "   ____..   ",
                "  |   \\  \\__",
                "   \\__|___| ",
                "    `-|`    "
            ],
            "W": [
                "    ____   ",
                " __/ __ \\  ",
                "(__| |__| | ",
                "   \\____/  "
            ],
            "NW": [
                " ..__     ",
                "|   \\  \\__ ",
                "|___|__/  ",
                " `-|`     "
            ]
        }
        super().__init__(
            x, y, art,
            durability=70,
            speed=10.0,
            acceleration=1.0,
            handling=0.2,
            braking_power=0.8,
            attachment_points={
                "engine_gun": {"level": "heavy", "offset_x": 0, "offset_y": -2},
                "left_exhaust_gun": {"level": "light", "offset_x": -2, "offset_y": 0},
                "right_exhaust_gun": {"level": "light", "offset_x": 2, "offset_y": 0}
            }
        )
        self.default_weapons = {
            "engine_gun": "wep_flamethrower"
        }
        self.max_attachments = 3
