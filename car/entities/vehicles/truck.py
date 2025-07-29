from .player_car import PlayerCar

class Truck(PlayerCar):
    """
    A big, durable American pickup truck. What it lacks in speed, it makes
    up for in sheer toughness and its capacity to carry heavy weapons.
    A true wasteland workhorse.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a classic pickup truck
        art = {
            # North (Facing Up)
            "N": [
                "  ▄▄███▄▄  ",
                " ▟███████▙ ",
                "(█)      (█)"
            ],
            # North-East
            "NE": [
                "    ▄▄████▄",
                "   ▟██▒▒▀▀█",
                "  (█)══(█)◥◣",
            ],
            # East (Facing Right)
            "E": [
                "   ▄▄█████ ",
                "  ▟██▒▒▀▀▀█",
                " (█)════(█)"
            ],
            # South-East
            "SE": [
                "  (█)════(█)",
                "  ◢◤▀▀▀▒▒██",
                "   ▀▀▀▀████"
            ],
            # South (Facing Down)
            "S": [
                "(█)      (█)",
                " ██▄▄▄▄▄▄██ ",
                " ▀▀▀▀▀▀▀▀▀▀ "
            ],
            # South-West
            "SW": [
                " (█)════(█) ",
                " ██▒▒▀▀▀◥◣ ",
                "  ████▀▀▀▀  "
            ],
            # West (Facing Left)
            "W": [
                "  █████▄▄   ",
                " █▀▀▀▒▒██▟  ",
                " (█)════(█) "
            ],
            # North-West
            "NW": [
                " ▄████▄▄    ",
                "█▀▀▒▒██▟   ",
                "◢◤(█)══(█)   "
            ]
        }
        super().__init__(
            x, y, art,
            durability=180,
            speed=2.8,
            acceleration=0.5,
            handling=0.08,
            braking_power=0.5,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"name": "Hood Gun", "level": "medium", "offset_x": 0, "offset_y": -2},
                "bed_gun": {"name": "Bed Gun", "level": "heavy", "offset_x": 0, "offset_y": 2}
            },
        )
        self.max_attachments = 7
        # Default loadout for this chassis
        self.default_weapons = {
            "hood_gun": "wep_hmg"
        }
        self.name = "Truck"
