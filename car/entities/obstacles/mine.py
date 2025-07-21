from ..obstacle import Obstacle

class Mine(Obstacle):
    def __init__(self, x, y):
        art = ["¤"]
        super().__init__(x, y, art, durability=1, damage=50, xp_value=5)
