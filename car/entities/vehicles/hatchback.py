from .player_car import PlayerCar

class Hatchback(PlayerCar):
    """
    A nimble and customizable starter vehicle. It's been given a visual overhaul
    for a more battle-ready appearance in the wasteland.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a more detailed look
        art = {
            # North (Facing Up)
            "N": [
                "  ▟▀▀▙  ",
                " █░░░░█ ",
                "◢██▄██◣",
                " (●) (●) "
            ],
            # North-East
            "NE": [
                "  ▄▄▟` ",
                " ▟░▒▒▙ ",
                "◢███◤` ",
                " (●)═(●) "
            ],
            # East (Facing Right)
            "E": [
                " ▄▄▄▟` ",
                " █░█▒▙ ",
                "◢█████ ",
                " (●)═(●)"
            ],
            # South-East
            "SE": [
                " (●)═(●) ",
                "◢███◣  ",
                " █░▒▒▟ ",
                "  ▀▀`  "
            ],
            # South (Facing Down)
            "S": [
                " (●) (●) ",
                "◥██▀██◤",
                " █▒▒▒▒█ ",
                "  ▜▄▄▛  "
            ],
            # South-West
            "SW": [
                " (●)═(●) ",
                "  ◢███◤",
                " ▙▒▒░█ ",
                "  `▀▀  "
            ],
            # West (Facing Left)
            "W": [
                " `▙▄▄▄ ",
                " ▟▒█░█ ",
                " █████◣",
                "  (●)═(●)"
            ],
            # North-West
            "NW": [
                " `▙▄▄  ",
                " ▟▒▒░▙ ",
                " `◥███◣",
                " (●)═(●) "
            ]
        }
        super().__init__(
            x, y, art,
            durability=90,
            speed=2.7,
            acceleration=0.7,
            handling=0.12,
            braking_power=0.75,
            # Attachment points for weapons
            attachment_points={
                "hood_gun": {"level": "light", "offset_x": 0, "offset_y": -2},
                "roof_rack": {"level": "light", "offset_x": 0, "offset_y": -1},
                "hatch_gun": {"level": "medium", "offset_x": 0, "offset_y": 2}
            }
        )
        self.max_attachments = 4
        # Default loadout for this chassis
        self.default_weapons = {
            "hatch_gun": "wep_shotgun"
        }
