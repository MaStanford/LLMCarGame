import random
from ..character import Character
from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Cow(Character):
    def __init__(self, x, y):
        art = [
            " ▗█▀█▖ ",
            " ▐◉ ◉▌ ",
            " ▝▄▄▄▘ ",
        ]
        super().__init__(x, y, art, durability=20, speed=0.25 * GLOBAL_SPEED_MULTIPLIER)
        self.xp_value = 3

    def update(self, game_state, world, dt):
        # Simple wandering AI
        if random.random() < 0.1:
            self.vx = random.uniform(-self.speed, self.speed)
            self.vy = random.uniform(-self.speed, self.speed)
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("FAUNA", 0), transparent_bg=True)
