from .player_car import PlayerCar

class Van(PlayerCar):
    """
    A large, durable box van. It's slow and handles like a boat, but it's
    tough as nails and can be outfitted with an arsenal of weapons, making
    it a mobile fortress.
    """
    def __init__(self, x, y):
        # 8-directional art for a large boxy cargo van
        art = {
            # North (Facing Up) — 5 lines × 7 chars
            "N": [
                " ▄░░░▄ ",
                "●█████●",
                " █████ ",
                " █████ ",
                "●▀███▀●",
            ],
            # South (Facing Down) — 5 lines × 7 chars (vertical mirror of N)
            "S": [
                "●▄███▄●",
                " █████ ",
                " █████ ",
                "●█████●",
                " ▀░░░▀ ",
            ],
            # East (Facing Right) — 3 lines × 11 chars
            "E": [
                " ▄████░▄▄ ",
                "●██████████●",
                " ▀████▓▀▀ ",
            ],
            # West (Facing Left) — 3 lines × 11 chars (horizontal mirror of E)
            "W": [
                " ▄▄░████▄ ",
                "●██████████●",
                " ▀▀▓████▀ ",
            ],
            # NE — 4 lines × 9 chars
            "NE": [
                "  ▄░░███ ",
                " ●█████▌ ",
                " ██████● ",
                " ▀████▀  ",
            ],
            # NW — 4 lines × 9 chars (horizontal mirror of NE)
            "NW": [
                " ███░░▄  ",
                " ▐█████● ",
                " ●██████ ",
                "  ▀████▀ ",
            ],
            # SE — 4 lines × 9 chars (vertical mirror of NE)
            "SE": [
                " ▄████▄  ",
                " ██████● ",
                " ●█████▌ ",
                "  ▀░░███ ",
            ],
            # SW — 4 lines × 9 chars (vertical mirror of NW)
            "SW": [
                "  ▄████▄ ",
                " ●██████ ",
                " ▐█████● ",
                " ███░░▀  ",
            ],
        }
        super().__init__(
            x, y, art,
            durability=150,
            speed=5.25,
            acceleration=2.0,
            handling=1.2,
            braking_power=3.0,
            # Attachment points for weapons
            attachment_points={
                "roof_rack": {"name": "Roof Rack", "level": "heavy", "offset_x": 0, "offset_y": -1},
                "side_gun_left": {"name": "Left Side Gun", "level": "medium", "offset_x": -2, "offset_y": 0},
                "side_gun_right": {"name": "Right Side Gun", "level": "medium", "offset_x": 2, "offset_y": 0}
            },
        )
        self.max_attachments = 6
        # Default loadout for this chassis
        self.default_weapons = {
            "side_gun_left": "wep_shotgun",
            "side_gun_right": "wep_shotgun"
        }
        self.name = "Van"
