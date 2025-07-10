from ..obstacle import Obstacle
from ...data.pickups import PICKUP_GAS

class OilBarrel(Obstacle):
    def __init__(self, x, y):
        art = [
            " ___ ",
            "|   |",
            "|___|",
        ]
        super().__init__(
            x, y, art,
            durability=15,
            damage=10,
            xp_value=5,
            drop_item=PICKUP_GAS,
            drop_rate=0.2,
            cash_value=5
        )
