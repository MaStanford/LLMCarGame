from .player_car import PlayerCar

class Truck(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  ________  ",
                " |  ____  | ",
                " | |    | | ",
                " | |____| | ",
                "  \\______/  "
            ],
            "NE": [
                "  ________. ",
                " |  ____/ | ",
                " | |    | | ",
                " | |____|/  ",
                "  \\______/   "
            ],
            "E": [
                "  ________ ",
                " |        |",
                " |________|",
                "   | O  O | "
            ],
            "SE": [
                " .________  ",
                " | \\____  | ",
                " | |    | | ",
                "  \\|____| | ",
                "   \\______/  "
            ],
            "S": [
                "  ________  ",
                " |        | ",
                " | |    | | ",
                " | |____| | ",
                "  \\______/  "
            ],
            "SW": [
                "   .________ ",
                "  | \\____  |",
                "  | |    | |",
                "   \\|____| |",
                "    \\______/ "
            ],
            "W": [
                "  ________ ",
                " |        |",
                " |________|",
                "   | O  O | "
            ],
            "NW": [
                "   ________.",
                "  |____  |",
                "  | |    | |",
                "   \\|____| |",
                "    \\______/ "
            ]
        }
        super().__init__(
            x, y, art,
            durability=180,
            speed=6.0,
            acceleration=0.5,
            handling=0.08,
            braking_power=0.5,
            attachment_points={
                "hood_gun": {"level": "heavy", "offset_x": 0, "offset_y": -3},
                "roof_rack": {"level": "heavy", "offset_x": 0, "offset_y": -1},
                "bed_gun": {"level": "heavy", "offset_x": 0, "offset_y": 3},
                "front_bumper_gun": {"level": "medium", "offset_x": 0, "offset_y": -4},
                "rear_bumper_gun": {"level": "medium", "offset_x": 0, "offset_y": 4}
            }
        )
        self.default_weapons = {
            "hood_gun": "wep_hmg"
        }
