from .player_car import PlayerCar

class Motorcycle(PlayerCar):
    """
    A fast and nimble motorcycle, perfect for weaving through hazards.
    It's fragile but boasts incredible speed and handling.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a motorcycle
        art = {
            # North (Facing Up) - 4 lines x 3 chars, front wheel at top
            "N": [
                " ◉ ",
                " █ ",
                "▐█▌",
                " ◉ "
            ],
            # North-East - 3 lines x 4 chars, front wheel upper-right
            "NE": [
                "  ▌◉",
                " █▌ ",
                "◉▐  "
            ],
            # East (Facing Right) - 2 lines x 5 chars, front wheel on right
            "E": [
                " ▐██ ",
                "◉ █ ◉"
            ],
            # South-East - 3 lines x 4 chars, vertical mirror of NE
            "SE": [
                "◉▐  ",
                " █▌ ",
                "  ▌◉"
            ],
            # South (Facing Down) - 4 lines x 3 chars, vertical mirror of N
            "S": [
                " ◉ ",
                "▐█▌",
                " █ ",
                " ◉ "
            ],
            # South-West - 3 lines x 4 chars, horizontal mirror of SE
            "SW": [
                "  ▌◉",
                " ▐█ ",
                "◉▐  "
            ],
            # West (Facing Left) - 2 lines x 5 chars, horizontal mirror of E
            "W": [
                " ██▌ ",
                "◉ █ ◉"
            ],
            # North-West - 3 lines x 4 chars, horizontal mirror of NE
            "NW": [
                "◉▐  ",
                " ▐█ ",
                "  ▌◉"
            ]
        }
        super().__init__(
            x, y, art,
            durability=40,
            speed=10.5,
            acceleration=6.0,
            handling=3.0,
            braking_power=8.0,
            weapon_aim_speed=1.5,
            weight=300,
            # Attachment points for weapons
            attachment_points={
                "front_gun": {"name": "Front Gun", "level": "light", "offset_x": 0, "offset_y": -1},
                "rear_gun": {"name": "Rear Gun", "level": "light", "offset_x": 0, "offset_y": 1}
            },
        )
        self.max_attachments = 2
        # Default loadout for this chassis
        self.default_weapons = {
            "front_gun": "wep_pistol"
        }
        self.name = "Motorcycle"
