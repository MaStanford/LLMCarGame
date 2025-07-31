import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_ram_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class RustBucket(Vehicle):
    """
    A volatile, ram-focused vehicle of the Rust Prophets.
    Its only goal is to collide with the player. Explodes on death.
    """
    def __init__(self, x, y):
        # New art for a beat-up 70s American sedan
        art = [
            "   ▄▄▄▄▄▄▄   ",
            "  ▟█░▒▒▒░█▙ ",
            " ██▄▄▄▄▄▄██ ",
            " (O)▀▀▀▀▀(X) "
        ]
        super().__init__(x, y, art, durability=45, speed=9.3 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.4, handling=0.08)
        self.name = "Rust Bucket"
        self.phases = [
            {"name": "Kamikaze", "duration": (10, 10), "behavior": "RAM", "next_phases": {"Kamikaze": 1.0}}
        ]
        self._initialize_ai()
        # This vehicle could have an on_death callback that creates an explosion

    def _initialize_ai(self):
        """Initializes the AI state."""
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        """Updates the vehicle's state and AI logic each frame."""
        # This AI is simple, it just rams forever.
        behavior = self.current_phase["behavior"]
        if behavior == "RAM":
            _execute_ram_behavior(self, game_state, self)
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        """Draws the vehicle on the screen."""
        from ...rendering.draw_utils import draw_sprite
        # Note the custom color pair for this faction
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_RUST", 0), transparent_bg=True)
