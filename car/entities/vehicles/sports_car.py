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
            # North (Facing Up) - 5 lines x 5 chars
            # Long axis vertical, nose at top, rear at bottom
            "N": [
                " ▄▀▄ ",
                "●▓▓▓●",
                "▐▓░▓▐",
                "●▓▓▓●",
                " ▀▄▀ ",
            ],
            # South (Facing Down) - 5 lines x 5 chars
            # Vertically mirrored N: nose at bottom, rear at top
            "S": [
                " ▄▀▄ ",
                "●▓▓▓●",
                "▐▓░▓▐",
                "●▓▓▓●",
                " ▀▄▀ ",
            ],
            # East (Facing Right) - 3 lines x 9 chars
            # Long axis horizontal, nose on right
            "E": [
                " ●▄▓▓▓▄▀ ",
                " ▐▓▓░▓▓▓▌",
                " ●▀▓▓▓▀▄ ",
            ],
            # West (Facing Left) - 3 lines x 9 chars
            # Horizontally mirrored E: nose on left
            "W": [
                " ▀▄▓▓▓▄● ",
                "▐▓▓▓░▓▓▐ ",
                " ▄▀▓▓▓▀● ",
            ],
            # NE (45-deg up-right) - 4 lines x 7 chars
            "NE": [
                "  ▄▀▓▓●",
                " ▐▓▓░▓▌",
                "●▓▓▓▓▌ ",
                " ▀▄●   ",
            ],
            # NW (45-deg up-left) - 4 lines x 7 chars
            # Horizontally mirrored NE
            "NW": [
                "●▓▓▀▄  ",
                "▐▓░▓▓▐ ",
                " ▐▓▓▓▓●",
                "   ●▄▀ ",
            ],
            # SE (45-deg down-right) - 4 lines x 7 chars
            # Vertically mirrored NE
            "SE": [
                " ▄▀●   ",
                "●▓▓▓▓▌ ",
                " ▐▓▓░▓▌",
                "  ▀▄▓▓●",
            ],
            # SW (45-deg down-left) - 4 lines x 7 chars
            # Horizontally mirrored SE
            "SW": [
                "   ●▀▄ ",
                " ▐▓▓▓▓●",
                "▐▓░▓▓▐ ",
                "●▓▓▄▀  ",
            ],
        }
        super().__init__(
            x, y, art,
            durability=80,
            speed=9.75,
            acceleration=4.0,
            handling=2.2,
            braking_power=5.5,
            weapon_aim_speed=1.2,
            attachment_points={
                "hood_gun": {"name": "Hood Gun", "level": "light", "offset_x": 0, "offset_y": -2},
                "spoiler_gun": {"name": "Spoiler Gun", "level": "medium", "offset_x": 0, "offset_y": 2}
            },
        )
        self.max_attachments = 4
        # Default loadout for this chassis
        self.default_weapons = {
            "hood_gun": "wep_lmg"
        }
        self.name = "Sports Car"
