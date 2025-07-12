from ..obstacle import Obstacle

class ScrapBarricade(Obstacle):
    def __init__(self, x, y):
        art = [
            " <|#/#|#\\#|>",
            " <|#\\#|#/#|>"
        ]
        super().__init__(
            x, y, art,
            durability=200,
            damage=30,
            xp_value=15,
            cash_value=15,
            drop_item="ammo_bullet",
            drop_rate=0.2
        )
