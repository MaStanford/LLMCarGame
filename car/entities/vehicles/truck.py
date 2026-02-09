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
            # North (Facing Up) — 5×7 — cab at top, bed below
            "N": [
                " ▄░░░▄ ",
                "██░░░██",
                "██▓▓▓██",
                "██▓▓▓██",
                " ▀███▀ ",
            ],
            # South (Facing Down) — 5×7 — vertical mirror of N
            "S": [
                " ▄███▄ ",
                "██▓▓▓██",
                "██▓▓▓██",
                "██░░░██",
                " ▀░░░▀ ",
            ],
            # East (Facing Right) — 3×11 — cab on right, bed on left
            "E": [
                "▄██▄▄▄██▄░▄",
                "▓▓▓█▓▓█▓░░▌",
                "▀██▀▀▀██▀░▀",
            ],
            # West (Facing Left) — 3×11 — horizontal mirror of E
            "W": [
                "▄░▄██▄▄▄██▄",
                "▐░░▓█▓▓█▓▓▓",
                "▀░▀██▀▀▀██▀",
            ],
            # North-East (diagonal) — 4×9 — cab at upper-right
            "NE": [
                "  ▄▄░░▄██",
                " ▓▓░░▓█▌ ",
                "██▓▓▓▓▌  ",
                " ▀██▀▀   ",
            ],
            # North-West (diagonal) — 4×9 — horizontal mirror of NE
            "NW": [
                "██▄░░▄▄  ",
                " ▐█▓░░▓▓ ",
                "  ▐▓▓▓▓██",
                "   ▀▀██▀ ",
            ],
            # South-East (diagonal) — 4×9 — vertical mirror of NE
            "SE": [
                " ▄██▄▄   ",
                "██▓▓▓▓▌  ",
                " ▓▓░░▓█▌ ",
                "  ▀▀░░▀██",
            ],
            # South-West (diagonal) — 4×9 — vertical mirror of NW
            "SW": [
                "   ▄▄██▄ ",
                "  ▐▓▓▓▓██",
                " ▐█▓░░▓▓ ",
                "██▀░░▀▀  ",
            ],
        }
        super().__init__(
            x, y, art,
            durability=180,
            speed=4.2,
            acceleration=2.5,
            handling=1.3,
            braking_power=3.5,
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
