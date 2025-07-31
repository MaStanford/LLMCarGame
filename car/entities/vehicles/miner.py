from ..vehicle import Vehicle
from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Miner(Vehicle):
    """
    A heavy, armored vehicle that lays mines.
    """
    def __init__(self, x, y):
        art = {
            "N": [
                " /MM\\ ",
                "|MMMM|",
                " \\MM/ "
            ]
        }
        super().__init__(x, y, art, durability=150, speed=2.85 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.3, handling=0.05)
        self.name = "Miner"
        self.is_major_enemy = True
        self.ai_state = {
            "phases": [
                {"duration": 150, "behavior": "deploy_mine", "next": {"chase": 1.0}},
                {"duration": 300, "behavior": "chase", "next": {"deploy_mine": 1.0}},
            ]
        }