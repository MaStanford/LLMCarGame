from .base import Entity
import logging

class Character(Entity):
    def __init__(self, x, y, art, durability, speed):
        super().__init__(x, y, art, durability)
        self.speed = speed
        self.width = max(len(line) for line in art) if art else 0
        self.height = len(art) if art else 0
        self.angle = 0.0

    def update(self, game_state, world, dt):
        # To be implemented by subclasses
        pass
