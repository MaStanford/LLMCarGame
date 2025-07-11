from .player_car import PlayerCar

class SportsCar(PlayerCar):
    """
    A fast and agile sports car, modeled after old-world classics.
    It sacrifices armor for superior speed and handling, perfect for a driver
    who values performance over brute force.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a classic sports car
        art = {
            # North (Facing Up)
            "N": [
                "  ▄▄██▄▄  ",
                " ▟██░░██▙ ",
                "  (●) (●)  "
            ],
            # North-East
            "NE": [
                "   ▄▄██▄▄ ",
                "  ▟██░░██▙",
                " ◢◤` (●)(●)",
            ],
            # East (Facing Right)
            "E": [
                "  ▄▄▄▄▄▄ ",
                " ▟██░░▒▒█",
                " (●)══(●)"
            ],
            # South-East
            "SE": [
                "  (●) (●) ",
                "◢██████▙",
                "◥██████◤"
            ],
            # South (Facing Down)
            "S": [
                " (●)══(●) ",
                " ████████ ",
                "  ▀▄▄▄▄▀  "
            ],
            # South-West
            "SW": [
                " (●) (●)  ",
                "▟██████◣",
                "◥██████◤ "
            ],
            # West (Facing Left)
            "W": [
                " ▄▄▄▄▄▄  ",
                "█▒▒░░██▟ ",
                "(●)══(●) "
            ],
            # North-West
            "NW": [
                " ▄▄██▄▄   ",
                "▟██░░██▙  ",
                "(●)(●) `◥◣ "
            ]
        }
        super().__init__(
            x, y, art,
            durability=80,
            speed=9.0,
            acceleration=0.8,
            handling=0.15,
            braking_power=0.6,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"level": "light", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"level": "not_installed", "offset_x": 0, "offset_y": -1},
                "left_fender": {"level": "not_installed", "offset_x": -2, "offset_y": 0},
                "right_fender": {"level": "not_installed", "offset_x": 2, "offset_y": 0}
            }
        )
        self.max_attachments = 4
        # Default loadout for this chassis
        self.default_weapons = {
            "hood_gun": "wep_lmg"
        }
