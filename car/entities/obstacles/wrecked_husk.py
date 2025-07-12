from ..obstacle import Obstacle

class WreckedHusk(Obstacle):
    def __init__(self, x, y):
        art = [
            "  ▄▟▀▀▙▄  ",
            " █░███░█ ",
            "(●)▀▀▀(⎐)"
        ]
        super().__init__(
            x, y, art,
            durability=100,
            damage=40,
            xp_value=20,
            cash_value=25,
            drop_item="repair_kit",
            drop_rate=0.5
        )
