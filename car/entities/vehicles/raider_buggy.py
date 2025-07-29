import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_strafe_behavior, _execute_ram_behavior

class RaiderBuggy(Vehicle):
    """
    A fast, aggressive buggy used by the Crimson Cartel.
    It harasses from a distance before closing in for a ramming attack.
    """
    def __init__(self, x, y):
        art = [
            "  ▄-▲-▄  ",
            " ▗█-█-█▖ ",
            "(●)---(●)"
        ]
        super().__init__(x, y, art, durability=40, speed=6.0, acceleration=0.7, handling=0.8)
        self.name = "Raider Buggy"
        self.xp_value = 15
        self.cash_value = 20
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.15
        self.phases = [
            {"name": "Harass", "duration": (3, 5), "behavior": "STRAFE", "next_phases": {"Ram": 0.6, "Harass": 0.4}},
            {"name": "Ram", "duration": (2, 3), "behavior": "RAM", "next_phases": {"Harass": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        self.phase_timer -= dt

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        behavior = self.current_phase["behavior"]
        if behavior == "STRAFE":
            _execute_strafe_behavior(self, game_state, self)
        elif behavior == "RAM":
            _execute_ram_behavior(self, game_state, self)
        
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_CRIMSON", 0), transparent_bg=True)
