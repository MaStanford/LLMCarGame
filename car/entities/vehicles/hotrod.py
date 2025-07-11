from .player_car import PlayerCar

class Hotrod(PlayerCar):
    """
    A classic wasteland hotrod, rebuilt for speed and style. Features a long
    engine block, exposed side exhausts, and massive rear wheels.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a classic hotrod look
        art = {
            # North (Facing Up)
            "N": [
                "  ▄▄█▄▄  ",
                " ▗██▆██▖ ",
                "  ◥█░█◤  ",
                " (█) (█) "
            ],
            # North-East
            "NE": [
                "    ▄▄▟` ",
                "   ▟▆▒▙  ",
                " ═<◤██◤` ",
                " (●)═(█) "
            ],
            # East (Facing Right)
            "E": [
                "   ▄▄▄▄▄◣",
                "  ▟▆██░█ ",
                " ═<════█ ",
                " (●)══(█)"
            ],
            # South-East
            "SE": [
                " (●)═(█) ",
                " ═<◣██◣ ",
                "   ▜▒▆▟ ",
                "    ▀▀`  "
            ],
            # South (Facing Down)
            "S": [
                " (█) (█) ",
                " ▄██▀██▄ ",
                " ▀█▒▒▒█▀ ",
                "   ▀▀▀   "
            ],
            # South-West
            "SW": [
                " (█)═(●) ",
                "  ◢██◢<═ ",
                "  ▙▆▒▟  ",
                "  `▀▀    "
            ],
            # West (Facing Left)
            "W": [
                " ◢▄▄▄▄▄   ",
                " █░██▆▙  ",
                " █════<═ ",
                " (█)══(●)"
            ],
            # North-West
            "NW": [
                " `▙▄▄    ",
                "  ▟▒▆▙   ",
                " `◥██◥<═ ",
                " (█)═(●) "
            ]
        }
        super().__init__(
            x, y, art,
            durability=70,
            speed=10.0,
            acceleration=1.0,
            handling=0.2,
            braking_power=0.8,
            # Attachment points for weapons
            attachment_points={
                "engine_gun": {"level": "heavy", "offset_x": 0, "offset_y": -2},
                "left_exhaust_gun": {"level": "light", "offset_x": -2, "offset_y": 0},
                "right_exhaust_gun": {"level": "light", "offset_x": 2, "offset_y": 0}
            }
        )
        self.max_attachments = 3
        # Default loadout for this chassis
        self.default_weapons = {
            "engine_gun": "wep_flamethrower"
        }
