from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, x, y, art, durability):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.art = art
        self.width = max(len(line) for line in art) if art else 0
        self.height = len(art) if art else 0
        self.durability = durability
        self.max_durability = durability

    @abstractmethod
    def update(self, game_state, world):
        pass

    @abstractmethod
    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        pass
