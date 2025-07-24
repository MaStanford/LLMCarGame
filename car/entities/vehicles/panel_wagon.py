from .player_car import PlayerCar

class PanelWagon(PlayerCar):
    """
    A slow but incredibly durable panel wagon. It serves as a mobile fortress,
    boasting numerous attachment points for heavy-duty hardware.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a panel wagon
        art = {
            # North (Facing Up)
            "N": [
                " ▄██████▄ ",
                "██▀───-▀██",
                "█▛▀▀▀▀▀▀▀▜█",
                " (●)   (●) "
            ],
            # North-East
            "NE": [
                "  ▄████▄▄ ",
                " ████▒▒▒█ ",
                "█▛▀▀▀██◤` ",
                " (●)══(●) "
            ],
            # East (Facing Right)
            "E": [
                "  ▄██████▄",
                " ▐██▒▒▒▒▒█",
                " █▀▀▀▀▀▀▀█",
                " (●)═══(●)"
            ],
            # South-East
            "SE": [
                " (●)══(●) ",
                "█▄▄▄██◣  ",
                " ▐██▒▒▒█ ",
                "  ▀████▀  "
            ],
            # South (Facing Down)
            "S": [
                " (●)   (●) ",
                "█▄▄▄▄▄▄▄▄▄█",
                "███▅█▅███",
                " ▀█████▀ "
            ],
            # South-West
            "SW": [
                "  (●)══(●) ",
                "  ◢██▄▄▄█",
                " █▒▒▒██▌ ",
                "  ▀████▀  "
            ],
            # West (Facing Left)
            "W": [
                " ▄██████▄  ",
                "█▒▒▒▒▒██▌ ",
                "█▀▀▀▀▀▀▀█ ",
                "(●)═══(●) "
            ],
            # North-West
            "NW": [
                "  ▄▄████▄  ",
                " █▒▒▒████ ",
                " `◥██▀▀▀▛█ ",
                "  (●)══(●) "
            ]
        }
        super().__init__(
            x, y, art,
            durability=140,
            speed=3.0,
            acceleration=0.55,
            handling=0.09,
            braking_power=0.55,
            # Attachment points for weapons
            attachment_points={
                "roof_rack": {"name": "Roof Rack", "level": "medium", "offset_x": 0, "offset_y": -1},
                "side_gun_left": {"name": "Left Side Gun", "level": "light", "offset_x": -2, "offset_y": 0},
                "side_gun_right": {"name": "Right Side Gun", "level": "light", "offset_x": 2, "offset_y": 0}
            },
        )
        self.max_attachments = 6
        # Default loadout for this chassis
        self.default_weapons = {
            "roof_rack": "wep_hmg"
        }
        self.name = "Panel Wagon"
