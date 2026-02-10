from .player_car import PlayerCar

class Sedan(PlayerCar):
    """
    A balanced four-door sedan. A reliable and versatile choice for any
    wasteland journeyman, offering a good mix of speed, armor, and firepower.
    """
    def __init__(self, x, y):
        # 8-directional art: sedan (medium, balanced car)
        # N/S: 5 lines x 5 chars | E/W: 3 lines x 9 chars | diags: 4 lines x 7 chars
        art = {
            # North (Facing Up) - hood at top, trunk at bottom
            "N": [
                " ▄▓▄ ",
                "●░░░●",
                "█▓▓▓█",
                "●███●",
                " ▀█▀ "
            ],
            # South (Facing Down) - hood at bottom, trunk at top
            "S": [
                " ▄█▄ ",
                "●███●",
                "█▓▓▓█",
                "●░░░●",
                " ▀▓▀ "
            ],
            # East (Facing Right) - hood on right
            "E": [
                "●▓███░▓▄ ",
                "█▓███▓░░▌",
                "●▓███░▓▀ "
            ],
            # West (Facing Left) - hood on left
            "W": [
                " ▄▓░███▓●",
                "▐░░▓███▓█",
                " ▀▓░███▓●"
            ],
            # North-East - front at upper-right
            "NE": [
                "  ▄▄░▓▄",
                " ●█░░▓█",
                "▐█▓▓██●",
                " ▀██▀  "
            ],
            # North-West - front at upper-left (horizontal mirror of NE)
            "NW": [
                "▄▓░▄▄  ",
                "█▓░░█● ",
                "●██▓▓█▌",
                "  ▀██▀ "
            ],
            # South-East - front at lower-right (vertical mirror of NE)
            "SE": [
                " ▄██▄  ",
                "▐█▓▓██●",
                " ●█░░▓█",
                "  ▀▀░▓▀"
            ],
            # South-West - front at lower-left (horizontal mirror of SE)
            "SW": [
                "  ▄██▄ ",
                "●██▓▓█▌",
                "█▓░░█● ",
                "▀▓░▀▀  "
            ]
        }
        super().__init__(
            x, y, art,
            durability=100,
            speed=7.5,
            acceleration=3.0,
            handling=1.8,
            braking_power=5.0,
            weapon_aim_speed=1.0,
            attachment_points={
                "hood_gun": {"name": "Hood Gun", "level": "light", "offset_x": 0, "offset_y": -2},
                "trunk_gun": {"name": "Trunk Gun", "level": "light", "offset_x": 0, "offset_y": 2}
            },
        )
        self.max_attachments = 5
        # Default loadout for this chassis
        self.default_weapons = {
            "hood_gun": "wep_lmg"
        }
        self.name = "Sedan"
