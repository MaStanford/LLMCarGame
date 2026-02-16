from .base import Entity
import logging

class Character(Entity):
    def __init__(self, x, y, art, durability, speed):
        super().__init__(x, y, art, durability)
        self.speed = speed
        self.width = max(len(line) for line in art) if art else 0
        self.height = len(art) if art else 0
        self.angle = 0.0

    def _move_with_terrain_check(self, world, dt):
        """Move the character, respecting impassable terrain (buildings, rocks, trees)."""
        next_x = self.x + self.vx * dt
        next_y = self.y + self.vy * dt

        if world is None:
            self.x = next_x
            self.y = next_y
            return

        center_x = next_x + self.width / 2
        center_y = next_y + self.height / 2
        terrain = world.get_terrain_at(center_x, center_y)

        if terrain.get("passable", True):
            self.x = next_x
            self.y = next_y
            return

        # Wall-slide: try X-only
        x_center = (self.x + self.vx * dt) + self.width / 2
        y_center = self.y + self.height / 2
        if world.get_terrain_at(x_center, y_center).get("passable", True):
            self.x += self.vx * dt
            self.vy *= 0.3
            return

        # Wall-slide: try Y-only
        x_center = self.x + self.width / 2
        y_center = (self.y + self.vy * dt) + self.height / 2
        if world.get_terrain_at(x_center, y_center).get("passable", True):
            self.y += self.vy * dt
            self.vx *= 0.3
            return

        # Fully blocked — stop
        self.vx = 0
        self.vy = 0

    def update(self, game_state, world, dt):
        # To be implemented by subclasses
        pass
