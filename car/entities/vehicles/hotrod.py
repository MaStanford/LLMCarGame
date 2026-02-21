from .player_car import PlayerCar

class Hotrod(PlayerCar):
    """
    A classic wasteland hotrod, rebuilt for speed and style. Features a long
    engine block, exposed side exhausts, and massive rear wheels.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a classic hotrod look
        art = {
            # North (Facing Up) 5x5 - hood at top, rear at bottom
            "N": [
                " ▄▒▄ ",
                "●▒▒▒●",
                "═▓░▓═",
                " ▓▓▓ ",
                "█▓▓▓█",
            ],
            # South (Facing Down) 5x5 - vertically mirrored N
            "S": [
                "█▓▓▓█",
                " ▓▓▓ ",
                "═▓░▓═",
                "●▒▒▒●",
                " ▀▒▀ ",
            ],
            # East (Facing Right) 3x9 - long hood to right, rear left
            "E": [
                "█═▓░▒▒▒▄●",
                "▓▓▓▓▓▒▒▒▒",
                "█═▓░▒▒▒▀●",
            ],
            # West (Facing Left) 3x9 - horizontally mirrored E
            "W": [
                "●▄▒▒▒░▓═█",
                "▒▒▒▒▓▓▓▓▓",
                "●▀▒▒▒░▓═█",
            ],
            # North-East (45 deg, up-right) 4x7
            "NE": [
                "  ▄▒▒●▒",
                " ●▒▒░▓ ",
                "═▓▓░▓▓ ",
                " █▓▓▓█ ",
            ],
            # North-West (45 deg, up-left) 4x7 - horizontally mirrored NE
            "NW": [
                "▒●▒▒▄  ",
                " ▓░▒▒● ",
                " ▓▓░▓▓═",
                " █▓▓▓█ ",
            ],
            # South-East (45 deg, down-right) 4x7 - vertically mirrored NE
            "SE": [
                " █▓▓▓█ ",
                "═▓▓░▓▓ ",
                " ●▒▒░▓ ",
                "  ▀▒▒●▒",
            ],
            # South-West (45 deg, down-left) 4x7 - horizontally mirrored SE
            "SW": [
                " █▓▓▓█ ",
                " ▓▓░▓▓═",
                " ▓░▒▒● ",
                "▒●▒▒▀  ",
            ],
        }
        super().__init__(
            x, y, art,
            durability=70,
            speed=10.2,
            acceleration=5.0,
            handling=2.5,
            braking_power=6.0,
            weapon_aim_speed=1.3,
            weight=1100,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"name": "Hood Gun", "level": "light", "offset_x": 0, "offset_y": -2},
                "spoiler_gun": {"name": "Spoiler Gun", "level": "medium", "offset_x": 0, "offset_y": 2}
            },
        )
        self.max_attachments = 3
        # Default loadout for this chassis
        self.default_weapons = {
            "hood_gun": "wep_flamethrower"
        }
        self.name = "Hotrod"
