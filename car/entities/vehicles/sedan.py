from .player_car import PlayerCar

class Sedan(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  ______  ",
                " /  __  \\ ",
                "|  |  |  |",
                " \\______/ "
            ],
            "NE": [
                "  ____..  ",
                " /   /  | ",
                "|___|  /  ",
                " `-|_/`   "
            ],
            "E": [
                "  ____ ",
                " / __ \\",
                "| |__| |",
                " \\____/"
            ],
            "SE": [
                "  ..____  ",
                " |  \\   \\ ",
                "  \\  |___| ",
                "   `\\_|-`  "
            ],
            "S": [
                "  ______  ",
                " /      \\ ",
                "|  |__|  |",
                " \\______/ "
            ],
            "SW": [
                "   ____.. ",
                "  |   \\   \\",
                "   \\__|___|",
                "    `-|`    "
            ],
            "W": [
                "   ____  ",
                "  / __ \\ ",
                " | |__| |",
                "  \\____/ "
            ],
            "NW": [
                " ..____   ",
                "|   \\   \\  ",
                "|___|__/   ",
                " `-|`     "
            ]
        }
        super().__init__(
            x, y, art,
            durability=100,
            speed=7.0,
            acceleration=0.6,
            handling=0.1,
            braking_power=0.7,
            attachment_points={
                "hood_gun": {"level": "medium", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"level": "light", "offset_x": 0, "offset_y": -1},
                "trunk_gun": {"level": "light", "offset_x": 0, "offset_y": 2},
                "left_fender": {"level": "not_installed", "offset_x": -2, "offset_y": 0},
                "right_fender": {"level": "not_installed", "offset_x": 2, "offset_y": 0}
            }
        )
        self.default_weapons = {
            "hood_gun": "wep_lmg"
        }
        self.max_attachments = 5
