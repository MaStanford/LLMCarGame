from ..obstacle import Obstacle

class TirePile(Obstacle):
    def __init__(self, x, y):
        art = [
            "   (O)   ",
            "  (O)(O)  ",
            " (O)(O)(O) "
        ]
        super().__init__(
            x, y, art,
            durability=30,
            damage=5,
            xp_value=3,
            cash_value=1,
            drop_item="repair_kit",
            drop_rate=0.05
        )
