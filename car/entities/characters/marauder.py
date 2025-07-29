import random
from ..character import Character
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_strafe_behavior

class Marauder(Character):
    def __init__(self, x, y):
        art = [
            "  __  ",
            " /..\\ ",
            "| > <|",
            " \\__/ ",
        ]
        super().__init__(x, y, art, durability=40, speed=0.35)
        self.xp_value = 20
        self.cash_value = 25
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.2
        self.phases = [
            {"name": "Chase", "duration": (2, 4), "behavior": "CHASE", "next_phases": {"Strafe": 1.0}},
            {"name": "Strafe", "duration": (3, 5), "behavior": "STRAFE", "next_phases": {"Chase": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

    def update(self, game_state, world, dt):
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
            
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
