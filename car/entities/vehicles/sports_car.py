from .player_car import PlayerCar

class SportsCar(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  .---.  ",
                " / o o \\ ",
                "|   ^   |",
                " `-----' "
            ],
            "NE": [
                "  .--.   ",
                " /o  /|  ",
                "|   | |  ",
                " `---' / "
            ],
            "E": [
                " ____  ",
                "|o  _> ",
                "|__/>  "
            ],
            "SE": [
                " .---.   ",
                "|  o \\  ",
                " \\__/ /  ",
                "  `--'   "
            ],
            "S": [
                " .-----. ",
                "| |   | |",
                " \\ o o / ",
                "  `---'  "
            ],
            "SW": [
                "   .---. ",
                "  / o  | ",
                " \\ \\__/  ",
                "  `--'   "
            ],
            "W": [
                "  ____ ",
                "<--o | ",
                " <__/| "
            ],
            "NW": [
                "   .--.  ",
                "  |\\  o\\ ",
                "  | |   |",
                "   \\ `---'"
            ]
        }
        super().__init__(
            x, y, art,
            durability=80,
            speed=9.0,
            acceleration=0.8,
            handling=0.15,
            braking_power=0.6,
            attachment_points={
                "hood_gun": {"level": "light", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"level": "not_installed", "offset_x": 0, "offset_y": -1},
                "left_fender": {"level": "not_installed", "offset_x": -2, "offset_y": 0},
                "right_fender": {"level": "not_installed", "offset_x": 2, "offset_y": 0}
            }
        )
        self.default_weapons = {
            "hood_gun": "wep_lmg"
        }
