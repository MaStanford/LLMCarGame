from .player_car import PlayerCar

class Motorcycle(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  o  ",
                " / \\ ",
                "| - |",
                " \\_/"
            ],
            "NE": [
                "  o__ ",
                " /  / ",
                "|  /  ",
                " \\/   "
            ],
            "E": [
                "  __ ",
                " o--\\",
                "  \\_/"
            ],
            "SE": [
                " __o  ",
                " \\  \\ ",
                "  \\  |",
                "   \\/ "
            ],
            "S": [
                "  _  ",
                " / \\ ",
                "| - |",
                "  o  "
            ],
            "SW": [
                "  o__ ",
                " /  / ",
                "|  /  ",
                " \\/   "
            ],
            "W": [
                "   __ ",
                " /--o ",
                " \\_/  "
            ],
            "NW": [
                " __o  ",
                " \\  \\ ",
                "  \\  |",
                "   \\/ "
            ]
        }
        super().__init__(
            x, y, art,
            durability=40,
            speed=12.0,
            acceleration=1.2,
            handling=0.3,
            braking_power=0.9,
            attachment_points={
                "handlebar_gun": {"level": "light", "offset_x": 0, "offset_y": -1},
                "saddlebag_gun": {"level": "light", "offset_x": 0, "offset_y": 1}
            }
        )
        self.default_weapons = {
            "handlebar_gun": "wep_pistol"
        }
