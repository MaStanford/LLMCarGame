import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_strafe_behavior, _execute_evade_behavior

class RustySedan(Vehicle):
    def __init__(self, x, y):
        art = [
            "   ____   ",
            "  / __ \\  ",
            " | |  | | ",
            " | |__| | ",
            "  \\____/  ",
        ]
        super().__init__(x, y, art, durability=20, speed=0.75, acceleration=0.5, handling=0.5)
        self.xp_value = 5
        self.cash_value = 10
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.05
        self.phases = [
            {"name": "Pursuit", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"DriveBy": 1.0}},
            {"name": "DriveBy", "duration": (3, 5), "behavior": "STRAFE", "next_phases": {"Pursuit": 0.7, "Reposition": 0.3}},
            {"name": "Reposition", "duration": (2, 3), "behavior": "EVADE", "next_phases": {"Pursuit": 1.0}}
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
        elif behavior == "STRAFE":
            _execute_strafe_behavior(self, game_state, self)
        elif behavior == "EVADE":
            _execute_evade_behavior(self, game_state, self)
            
        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
