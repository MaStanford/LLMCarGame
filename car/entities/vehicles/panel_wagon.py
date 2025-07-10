from .player_car import PlayerCar

class PanelWagon(PlayerCar):
    def __init__(self, x, y):
        art = {
            "N": [
                "  _________  ",
                " /   ___   \\ ",
                "|   /   \\   |",
                "|   \\___/   |",
                " \\_________/ "
            ],
            "NE": [
                "  _________. ",
                " /   ____/ | ",
                "|   /   |  | ",
                "|   \\___| /  ",
                " \\_______|/   "
            ],
            "E": [
                "  _________  ",
                " |         | ",
                " |_________| ",
                " | O     O | "
            ],
            "SE": [
                " ._________  ",
                " | \\____   \\ ",
                " |  |   \\   |",
                "  \\ |___/   |",
                "   \\|_______| "
            ],
            "S": [
                "  _________  ",
                " |         | ",
                " | |     | | ",
                " | |_____| | ",
                " |_________| "
            ],
            "SW": [
                "   ._________ ",
                "  | \\____   |",
                "  |  |   \\  |",
                "   \\ |___/  |",
                "    \\|______|"
            ],
            "W": [
                "  _________  ",
                " |         | ",
                " |_________| ",
                " | O     O | "
            ],
            "NW": [
                "   _________.",
                "  |____   / |",
                "  |   /   | |",
                "   \\ |___/  |",
                "    \\|______|"
            ]
        }
        super().__init__(
            x, y, art,
            durability=140,
            speed=6.5,
            acceleration=0.55,
            handling=0.09,
            braking_power=0.55,
            attachment_points={
                "hood_gun": {"level": "medium", "offset_x": 0, "offset_y": -3},
                "roof_rack": {"level": "heavy", "offset_x": 0, "offset_y": -1},
                "rear_door_gun": {"level": "light", "offset_x": 0, "offset_y": 3},
                "left_panel_gun": {"level": "medium", "offset_x": -3, "offset_y": 0},
                "right_panel_gun": {"level": "medium", "offset_x": 3, "offset_y": 0}
            }
        )
        self.default_weapons = {
            "roof_rack": "wep_hmg"
        }
