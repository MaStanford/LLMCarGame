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

    def update(self, game_state, world):
        # Obstacles are static by default, so no update logic is needed here.
        # This can be overridden by subclasses for moving obstacles.
        pass

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        logging.info(f"ENTITY_DRAW: Drawing obstacle {self.__class__.__name__} at ({self.x}, {self.y})")
        from ..rendering.draw_utils import draw_sprite
        
        screen_x = self.x - world_start_x
        screen_y = self.y - world_start_y
        
        # Basic culling
        if screen_x + self.width < 0 or screen_x > game_state.screen_width or \
           screen_y + self.height < 0 or screen_y > game_state.screen_height:
            return
            
        draw_sprite(stdscr, screen_y, screen_x, self.art, color_map.get("OBSTACLE", 0), transparent_bg=True)
