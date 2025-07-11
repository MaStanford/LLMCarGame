from .player_car import PlayerCar

class Van(PlayerCar):
    """
    A large, durable box van. It's slow and handles like a boat, but it's
    tough as nails and can be outfitted with an arsenal of weapons, making
    it a mobile fortress.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a classic box van
        art = {
            # North (Facing Up)
            "N": [
                "  ▄▄▄▄▄▄▄  ",
                " ▗█░░░░░░█▖ ",
                " █████████ ",
                " (●)═══(●) "
            ],
            # North-East
            "NE": [
                "   ▄▄▄▄▄▄▄▄",
                "  ▟░▒▀▀▀▀██",
                " █▒███████",
                "(●)════(●) "
            ],
            # East (Facing Right)
            "E": [
                "   ▄▄▄▄▄▄▄▄▄ ",
                "  ▟░▒███████",
                " █▒█████████",
                "(●)══════(●)"
            ],
            # South-East
            "SE": [
                "(●)════(●) ",
                " █████████",
                "  ▀▀▀▀▀▀██",
                "     ▀▀▀▀▀▀"
            ],
            # South (Facing Down)
            "S": [
                " (●)═══(●) ",
                " █████████ ",
                " █████▄▄██ ",
                " ▀▀▀▀▀▀▀▀▀ "
            ],
            # South-West
            "SW": [
                " (●)════(●)",
                "█████████ ",
                "██▀▀▀▀▀▀  ",
                "▀▀▀▀▀▀     "
            ],
            # West (Facing Left)
            "W": [
                " ▄▄▄▄▄▄▄▄▄   ",
                "███████▒░▟  ",
                "█████████▒█  ",
                "(●)══════(●) "
            ],
            # North-West
            "NW": [
                "▄▄▄▄▄▄▄▄   ",
                "██▀▀▀▀▒░▟  ",
                "████████▒█ ",
                " (●)════(●)"
            ]
        }
        super().__init__(
            x, y, art,
            durability=150,
            speed=5.0,
            acceleration=0.4,
            handling=0.07,
            braking_power=0.4,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"level": "heavy", "offset_x": 0, "offset_y": -3},
                "roof_rack": {"level": "heavy", "offset_x": 0, "offset_y": -1},
                "left_side_gun": {"level": "medium", "offset_x": -3, "offset_y": 0},
                "right_side_gun": {"level": "medium", "offset_x": 3, "offset_y": 0},
                "rear_gun": {"level": "light", "offset_x": 0, "offset_y": 3}
            }
        )
        self.max_attachments = 6
        # Default loadout for this chassis
        self.default_weapons = {
            "left_side_gun": "wep_shotgun",
            "right_side_gun": "wep_shotgun"
        }
