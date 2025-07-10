import random
from ..character import Character
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_stationary_behavior

class Bandit(Character):
    def __init__(self, x, y):
        art = [
            "  _  ",
            " / \\ ",
            "|o.o|",
            " \\_/ ",
        ]
        super().__init__(x, y, art, durability=10, speed=0.25)
        self.cash_value = 10
        self.phases = [
            {"name": "Charge", "duration": (3, 5), "behavior": "CHASE", "next_phases": {"Charge": 0.8, "Hesitate": 0.2}},
            {"name": "Hesitate", "duration": (1, 2), "behavior": "STATIONARY", "next_phases": {"Charge": 1.0}}
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
        elif behavior == "STATIONARY":
            _execute_stationary_behavior(self)
            
        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
