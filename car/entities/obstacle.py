from .base import Entity
import logging

class Obstacle(Entity):
    def __init__(self, x, y, art, durability, damage, xp_value=0, drop_item=None, drop_rate=0.0, cash_value=0):
        super().__init__(x, y, art, durability)
        self.damage = damage
        self.xp_value = xp_value
        self.drop_item = drop_item
        self.drop_rate = drop_rate
        self.cash_value = cash_value
        self.width = max(len(line) for line in art) if art else 0
        self.height = len(art) if art else 0
        self.angle = 0.0

    def update(self, game_state, world, dt):
        # Obstacles are static by default, so no update logic is needed here.
        # This can be overridden by subclasses for moving obstacles.
        pass
