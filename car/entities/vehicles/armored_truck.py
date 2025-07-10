import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior

class ArmoredTruck(Vehicle):
    def __init__(self, x, y):
        art = [
            "   /---\\",
            "  /____\\",
            " |[][][]|",
            " (o)__(o)",
        ]
        super().__init__(x, y, art, durability=100, speed=0.5, acceleration=0.3, handling=0.3)
        self.phases = [
            {"name": "ProbingAttack", "duration": (5, 7), "behavior": "CHASE", "next_phases": {"ProbingAttack": 1.0}},
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

    def update(self, game_state, world):
        self.phase_timer -= 1 / 30.0 # Assuming 30 FPS

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
            
        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
