from .player_car import PlayerCar

class PanelWagon(PlayerCar):
    """
    A slow but incredibly durable panel wagon. It serves as a mobile fortress,
    boasting numerous attachment points for heavy-duty hardware.
    """
    def __init__(self, x, y):
        # Redesigned 8-directional art set for a panel wagon
        art = {
            # North (Facing Up) — 5 lines × 7 chars
            "N": [
                "  ▄█▄  ",
                " █░░░█ ",
                " █▒▒▒█ ",
                " █▓▓▓█ ",
                " ●▀█▀● ",
            ],
            # South (Facing Down) — 5 lines × 7 chars (vertical mirror of N)
            "S": [
                " ●▄█▄● ",
                " █▓▓▓█ ",
                " █▒▒▒█ ",
                " █░░░█ ",
                "  ▀█▀  ",
            ],
            # East (Facing Right) — 3 lines × 11 chars
            "E": [
                " ▄█▓▒░░▀▄ ",
                " ●██████●▌",
                " ▀█▓▒░░▄▀ ",
            ],
            # West (Facing Left) — 3 lines × 11 chars (horizontal mirror of E)
            "W": [
                " ▄▀░░▒▓█▄ ",
                "▐●██████● ",
                " ▀▄░░▒▓█▀ ",
            ],
            # North-East — 4 lines × 9 chars
            "NE": [
                "  ▄░░▀▌ ",
                " █▒▒██▀ ",
                " █▓██▀  ",
                " ●▀ ▀●  ",
            ],
            # North-West — 4 lines × 9 chars (horizontal mirror of NE)
            "NW": [
                " ▐▀░░▄  ",
                " ▀██▒▒█ ",
                "  ▀██▓█ ",
                "  ●▀ ▀● ",
            ],
            # South-East — 4 lines × 9 chars (vertical mirror of NE)
            "SE": [
                " ●▄ ▄●  ",
                " █▓██▄  ",
                " █▒▒██▄ ",
                "  ▀░░▄▌ ",
            ],
            # South-West — 4 lines × 9 chars (horizontal mirror of SE)
            "SW": [
                "  ●▄ ▄● ",
                "  ▄██▓█ ",
                " ▄██▒▒█ ",
                " ▐▄░░▀  ",
            ],
        }
        super().__init__(
            x, y, art,
            durability=140,
            speed=4.5,
            acceleration=2.5,
            handling=1.4,
            braking_power=3.5,
            # Attachment points for weapons
            attachment_points={
                "roof_rack": {"name": "Roof Rack", "level": "medium", "offset_x": 0, "offset_y": -1},
                "side_gun_left": {"name": "Left Side Gun", "level": "light", "offset_x": -2, "offset_y": 0},
                "side_gun_right": {"name": "Right Side Gun", "level": "light", "offset_x": 2, "offset_y": 0}
            },
        )
        self.max_attachments = 6
        # Default loadout for this chassis
        self.default_weapons = {
            "roof_rack": "wep_hmg"
        }
        self.name = "Panel Wagon"
