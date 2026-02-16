import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import execute_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class RustySedan(Vehicle):
    def __init__(self, x, y):
        art = [
            "   ____   ",
            "  / __ \  ",
            " | |  | | ",
            " | |__| | ",
            "  \____/  ",
        ]
        super().__init__(x, y, art, durability=20, speed=6.75 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.5, handling=0.5)
        self.name = "Rusty Sedan"
        self.xp_value = 5
        self.cash_value = 10
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.05
        self.collision_damage = 3
        self.shoot_damage = 2
        self.phases = [
            {"name": "Pursuit", "duration": (4, 6), "behavior": "CHASE", "next_phases": {"DriveBy": 1.0}},
            {"name": "DriveBy", "duration": (3, 5), "behavior": "SHOOT", "next_phases": {"Pursuit": 0.5, "Reposition": 0.5}},
            {"name": "Reposition", "duration": (2, 3), "behavior": "EVADE", "next_phases": {"Pursuit": 1.0}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

    def update(self, game_state, world, dt):
        self.ai_state["elapsed"] = self.ai_state.get("elapsed", 0) + dt

        self.phase_timer -= dt

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(self.current_phase["duration"][0], self.current_phase["duration"][1])

        execute_behavior(self.current_phase["behavior"], self, game_state, self)

        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY", 0), transparent_bg=True)
