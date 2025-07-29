from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, x, y, art, durability):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.art = art
        self.width = 0
        self.height = 0
        self.durability = durability
        self.max_durability = durability
        self.patrol_target_x = None
        self.patrol_target_y = None
        self.is_major_enemy = False
        self.patrol_target_x = None
        self.patrol_target_y = None

    @staticmethod
    def get_car_dimensions(car_art_list):
        """Calculates the height and max width across all directional sprites."""
        if not car_art_list or not car_art_list[0]:
            return 0, 0
        height = len(car_art_list[0])
        max_width = 0
        for art in car_art_list:
            if art:
                current_max_line_width = 0
                for line in art:
                    visual_width = 0
                    in_escape = False
                    for char in line:
                        if char == '<': in_escape = True; continue
                        if char == '>': in_escape = False; continue
                        if not in_escape: visual_width += 1
                    current_max_line_width = max(current_max_line_width, visual_width)
                max_width = max(max_width, current_max_line_width)
        return height, max_width

    @abstractmethod
    def update(self, game_state, world, dt):
        pass
import logging
