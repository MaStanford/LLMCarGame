from .player_car import PlayerCar

class Motorcycle(PlayerCar):
    """
    A fast and nimble motorcycle, perfect for weaving through hazards.
    It's fragile but boasts incredible speed and handling.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a motorcycle
        art = {
            # North (Facing Up)
            "N": [
                " ◒ ",
                "╭█╮",
                " │ ",
                " O "
            ],
            # North-East
            "NE": [
                "  ◒╗ ",
                " ╱█│ ",
                "O-╯  "
            ],
            # East (Facing Right)
            "E": [
                "  ◒═╗",
                " O═█╣",
                "  ╰═╝"
            ],
            # South-East
            "SE": [
                "O-╮  ",
                " ╲█│ ",
                "  ◒╝ "
            ],
            # South (Facing Down)
            "S": [
                " O ",
                " │ ",
                "╰█╯",
                " ◒ "
            ],
            # South-West
            "SW": [
                "  ╭-O",
                " │█╱ ",
                " ╚◒  "
            ],
            # West (Facing Left)
            "W": [
                "╔═◒  ",
                "╠█═O ",
                "╚═╯  "
            ],
            # North-West
            "NW": [
                " ╔◒  ",
                " │█╲ ",
                "  ╰-O"
            ]
        }
        super().__init__(
            x, y, art,
            durability=40,
            speed=10.5,
            acceleration=1.2,
            handling=0.3,
            braking_power=0.9,
            # Attachment points for weapons
            attachment_points={
                "front_gun": {"name": "Front Gun", "level": "light", "offset_x": 0, "offset_y": -1},
                "rear_gun": {"name": "Rear Gun", "level": "light", "offset_x": 0, "offset_y": 1}
            },
        )
        self.max_attachments = 2
        # Default loadout for this chassis
        self.default_weapons = {
            "handlebar_gun": "wep_pistol"
        }
        self.name = "Motorcycle"
