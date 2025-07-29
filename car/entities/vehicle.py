from .base import Entity
import logging

class Vehicle(Entity):
    def __init__(self, x, y, art, durability, speed, acceleration, handling):
        super().__init__(x, y, art, durability)
        self.speed = speed
        self.acceleration = acceleration
        self.handling = handling
        self.fuel = 100
        self.max_fuel = 100
        self.attachment_points = {}
        self.angle = 0.0
        
        if isinstance(art, dict):
            self.height, self.width = Entity.get_car_dimensions(list(art.values()))
        elif isinstance(art, list):
            self.width = max(len(line) for line in art) if art else 0
            self.height = len(art) if art else 0

    def update(self, game_state, world, dt):
        # To be implemented by subclasses
        pass
