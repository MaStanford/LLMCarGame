import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import execute_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Technical(Vehicle):
    """
    A versatile, gun-mounted pickup used by the Salvage Core.
    It balances direct pursuit with suppressive fire from a distance.
    """
    def __init__(self, x, y):
        art = [
            "  ▄▄▄    ",
            " █ ▆ █═╦╗",
            " (●)═(●) "
        ]
        super().__init__(x, y, art, durability=70, speed=8.25 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.5, handling=0.6)
        self.name = "Technical"
        self.xp_value = 25
        self.cash_value = 40
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.25
        self.collision_damage = 5
        self.shoot_damage = 4
        self.phases = [
            {"name": "Approach", "duration": (3, 5), "behavior": "CHASE", "next_phases": {"SuppressiveFire": 1.0}},
            {"name": "SuppressiveFire", "duration": (4, 6), "behavior": "SHOOT", "next_phases": {"Flank": 0.6, "Approach": 0.4}},
            {"name": "Flank", "duration": (3, 4), "behavior": "FLANK", "next_phases": {"SuppressiveFire": 0.7, "Approach": 0.3}}
        ]
        self._initialize_ai()

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        self.ai_state["elapsed"] = self.ai_state.get("elapsed", 0) + dt

        self.phase_timer -= dt

        if self.phase_timer <= 0:
            next_phase_options = list(self.current_phase["next_phases"].keys())
            next_phase_weights = list(self.current_phase["next_phases"].values())
            new_phase_name = random.choices(next_phase_options, weights=next_phase_weights, k=1)[0]
            self.current_phase = next((p for p in self.phases if p["name"] == new_phase_name), self.phases[0])
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        execute_behavior(self.current_phase["behavior"], self, game_state, self)

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_SALVAGE", 0), transparent_bg=True)
