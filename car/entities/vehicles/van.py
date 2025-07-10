from .player_car import PlayerCar

class Van(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  _______  ",
                " |  ___  | ",
                " | |   | | ",
                " | |___| | ",
                " |_______| "
            ],
            "NE": [
                "  _______. ",
                " |  ____/| ",
                " | |   | | ",
                " | |___|/  ",
                " |_____|   "
            ],
            "E": [
                "  _______  ",
                " |       | ",
                " |_______| ",
                " | O   O | "
            ],
            "SE": [
                " ._______  ",
                " |\\____  | ",
                " | |   | | ",
                "  \\|___| | ",
                "   |_____| "
            ],
            "S": [
                "  _______  ",
                " |       | ",
                " | |   | | ",
                " | |___| | ",
                " |_______| "
            ],
            "SW": [
                "   ._______ ",
                "  |\\____  |",
                "  | |   | |",
                "   \\|___| |",
                "    |_____|"
            ],
            "W": [
                "  _______  ",
                " |       | ",
                " |_______| ",
                " | O   O | "
            ],
            "NW": [
                "   _______.",
                "  |____  |",
                "  | |   | |",
                "   \\|___| |",
                "    |_____|"
            ]
        }
        super().__init__(
            x, y, art,
            durability=150,
            speed=5.0,
            acceleration=0.4,
            handling=0.07,
            braking_power=0.4,
            attachment_points={
                "hood_gun": {"level": "heavy", "offset_x": 0, "offset_y": -3},
                "roof_rack": {"level": "heavy", "offset_x": 0, "offset_y": -1},
                "left_side_gun": {"level": "medium", "offset_x": -3, "offset_y": 0},
                "right_side_gun": {"level": "medium", "offset_x": 3, "offset_y": 0},
                "rear_gun": {"level": "light", "offset_x": 0, "offset_y": 3}
            }
        )
        self.default_weapons = {
            "left_side_gun": "wep_shotgun",
            "right_side_gun": "wep_shotgun"
        }
