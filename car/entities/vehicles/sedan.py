from .player_car import PlayerCar

class Sedan(PlayerCar):
    """
    A balanced four-door sedan. A reliable and versatile choice for any
    wasteland journeyman, offering a good mix of speed, armor, and firepower.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a classic, wider sedan
        art = {
            # North (Facing Up) - Made wider
            "N": [
                "  ▄████▄  ",
                " ▗█░░░░█▖ ",
                " ██▒▒▒▒██ ",
                " (●)   (●) "
            ],
            # North-East - Adjusted for wider frame
            "NE": [
                "   ▄▄████▄ ",
                "  ▟░▒▒▒▒██▖",
                " █▒▒███◤` ",
                "(●)═══(●)  "
            ],
            # East (Facing Right) - Made longer to match new proportions
            "E": [
                "   ▄▄▄▄▄▄▄▄ ",
                "  ▟░▒▒▒▒▒▒█ ",
                " █▒▒▒▒▒▒▒▒█ ",
                "(●)══════(●)"
            ],
            # South-East - Adjusted for wider frame
            "SE": [
                "(●)═══(●)  ",
                " █▒▒███◣  ",
                "  ▜░▒▒▒▒██▖",
                "   ▀▀████▀ "
            ],
            # South (Facing Down) - Made wider
            "S": [
                " (●)   (●) ",
                " ████████ ",
                " ▀█▄▄▄▄█▀ ",
                "  ▀████▀  "
            ],
            # South-West - Adjusted for wider frame
            "SW": [
                "  (●)═══(●)",
                "  ◢███▒▒█ ",
                " ▗██▒▒▒▒░▟ ",
                " ▀████▀▀   "
            ],
            # West (Facing Left) - Made longer to match new proportions
            "W": [
                " ▄▄▄▄▄▄▄▄   ",
                " █▒▒▒▒▒▒░▟  ",
                " █▒▒▒▒▒▒▒▒█  ",
                "(●)══════(●) "
            ],
            # North-West - Adjusted for wider frame
            "NW": [
                " ▄████▄▄   ",
                "▗██▒▒▒▒░▟  ",
                " `◥███▒▒█  ",
                "  (●)═══(●) "
            ]
        }
        super().__init__(
            x, y, art,
            durability=100,
            speed=3.2,
            acceleration=0.6,
            handling=0.1,
            braking_power=0.7,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"level": "medium", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"level": "light", "offset_x": 0, "offset_y": -1},
                "trunk_gun": {"level": "light", "offset_x": 0, "offset_y": 2},
                "left_fender": {"level": "not_installed", "offset_x": -2, "offset_y": 0},
                "right_fender": {"level": "not_installed", "offset_x": 2, "offset_y": 0}
            }
        )
        self.max_attachments = 5
        # Default loadout for this chassis
        self.default_weapons = {
            "hood_gun": "wep_lmg"
        }
