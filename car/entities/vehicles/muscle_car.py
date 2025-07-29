import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_strafe_behavior, _execute_ram_behavior

class MuscleCar(Vehicle):
    """
    A classic, high-performance muscle car. It's fast, aggressive,
    and built for high-speed combat.
    """
    def __init__(self, x, y):
        # Art inspired by the iconic Fast & Furious muscle car
        art = [
            "   ▄▄█▀▀█▄▄   ",
            "  ▟██▆▆▆██▙  ",
            " ███████████ ",
            " (●)▀▀▀▀▀(●) "
        ]
        super().__init__(x, y, art, durability=85, speed=6.7, acceleration=0.9, handling=0.18)
        self.name = "Muscle Car"
        self.xp_value = 40
        self.cash_value = 75
        self.drop_item = "repair_kit"
        self.drop_rate = 0.1
        
        # Aggressive, multi-phase AI for a skilled driver
        self.phases = [
            {"name": "AggressiveChase", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"StrafeAndShoot": 1.0}},
            {"name": "StrafeAndShoot", "duration": (4, 6), "behavior": "STRAFE", "next_phases": {"AggressiveChase": 0.7, "RammingRun": 0.3}},
            {"name": "RammingRun", "duration": (2, 3), "behavior": "RAM", "next_phases": {"AggressiveChase": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        """Initializes the AI state."""
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

    def update(self, game_state, world, dt):
        """Updates the vehicle's state and AI logic each frame."""
        self.phase_timer -= dt

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        elif behavior == "STRAFE":
            _execute_strafe_behavior(self, game_state, self)
        elif behavior == "RAM":
            _execute_ram_behavior(self, game_state, self)
            
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        """Draws the vehicle on the screen."""
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
