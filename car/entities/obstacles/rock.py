from ..obstacle import Obstacle

class Rock(Obstacle):
    def __init__(self, x, y):
        art = [
            " ▗▄▓▄▖ ",
            "▐░▓▓░▌",
            " ▝▀▀▀▘ ",
        ]
        super().__init__(
            x, y, art,
            durability=50,
            damage=20,
            xp_value=2
        )
