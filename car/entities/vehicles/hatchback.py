from .player_car import PlayerCar

class Hatchback(PlayerCar):
    """
    A nimble and customizable starter vehicle. It's been given a visual overhaul
    for a more battle-ready appearance in the wasteland.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a more detailed look
        art = {
            # North (Facing Up) - 4 lines x 5 chars
            # Hood/nose at top, blunt hatch at bottom
            "N": [
                " ▄▀▄ ",
                "●░░░●",
                "●▓▓▓●",
                " █▄█ ",
            ],
            # South (Facing Down) - 4 lines x 5 chars
            # Vertically mirrored N: blunt hatch at top, nose at bottom
            "S": [
                " █▀█ ",
                "●▓▓▓●",
                "●░░░●",
                " ▀▄▀ ",
            ],
            # East (Facing Right) - 3 lines x 7 chars
            # Front/nose on right, blunt hatch on left
            "E": [
                " ●▄▄▄● ",
                "█▓░░░▀▌",
                " ●▀▀▀● ",
            ],
            # West (Facing Left) - 3 lines x 7 chars
            # Horizontally mirrored E: front/nose on left, hatch on right
            "W": [
                " ●▄▄▄● ",
                "▐▀░░░▓█",
                " ●▀▀▀● ",
            ],
            # North-East (45 degrees) - 3 lines x 6 chars
            # Nose upper-right, hatch lower-left
            "NE": [
                " ▄▄▀▌",
                "●░░▓█",
                "█▓●▀ ",
            ],
            # North-West (45 degrees) - 3 lines x 6 chars
            # Horizontal mirror of NE: nose upper-left, hatch lower-right
            "NW": [
                "▐▀▄▄ ",
                "█▓░░●",
                " ▀●▓█",
            ],
            # South-East (45 degrees) - 3 lines x 6 chars
            # Vertical mirror of NE: hatch upper-right, nose lower-left
            "SE": [
                "█▓●▄ ",
                "●░░▓█",
                " ▀▀▄▌",
            ],
            # South-West (45 degrees) - 3 lines x 6 chars
            # Horizontal mirror of SE / vertical mirror of NW
            "SW": [
                " ▄●▓█",
                "█▓░░●",
                "▐▄▀▀ ",
            ],
        }
        super().__init__(
            x, y, art,
            durability=90,
            speed=7.2,
            acceleration=3.5,
            handling=0.12,
            braking_power=5.5,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"name": "Hood Gun", "level": "light", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"name": "Roof Rack", "level": "light", "offset_x": 0, "offset_y": -1},
                "hatch_gun": {"name": "Hatch Gun", "level": "medium", "offset_x": 0, "offset_y": 1}
            },
            default_weapons={
                "hatch_gun": "wep_shotgun"
            }
        )
        self.max_attachments = 4
        self.name = "Hatchback"
