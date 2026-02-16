from ..obstacle import Obstacle

class Mine(Obstacle):
    """A stationary explosive device."""
    def __init__(self, x, y):
        art = ["(M)"]
        super().__init__(x, y, art, durability=1, damage=50, xp_value=10, drop_rate=0)
