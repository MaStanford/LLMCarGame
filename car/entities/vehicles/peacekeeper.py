import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import execute_behavior

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Peacekeeper(Vehicle):
    """
    A standard patrol vehicle from The Junction.
    It patrols a set area and gives chase only when provoked.
    """
    def __init__(self, x, y):
        art = [
            "    ▄█▄    ",
            " ▂▃▅█▅▃▂ ",
            " (●)═(●) "
        ]
        super().__init__(x, y, art, durability=80, speed=4.8 * GLOBAL_SPEED_MULTIPLIER, acceleration=0.5, handling=0.7)
        self.name = "Peacekeeper"
        self.xp_value = 10
        self.cash_value = 15
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.1
        self.collision_damage = 5
        self.shoot_damage = 3
        self.phases = [
            {"name": "Patrol", "duration": (5, 8), "behavior": "PATROL", "next_phases": {"Patrol": 1.0}},
            {"name": "Engage", "duration": (5, 8), "behavior": "CHASE", "next_phases": {"Shoot": 0.5, "Engage": 0.5}},
            {"name": "Shoot", "duration": (3, 5), "behavior": "SHOOT", "next_phases": {"Engage": 1.0}}
        ]
        self._initialize_ai()
        self.aggro_radius = 25

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        self.ai_state["elapsed"] = self.ai_state.get("elapsed", 0) + dt

        self.phase_timer -= dt

        dist_to_player = ((self.x - game_state.car_world_x)**2 + (self.y - game_state.car_world_y)**2)**0.5

        if dist_to_player <= self.aggro_radius and self.current_phase["name"] == "Patrol":
            # If player gets too close, engage
            self.current_phase = next((p for p in self.phases if p["name"] == "Engage"), self.phases[1])
            self.phase_timer = random.uniform(*self.current_phase["duration"])
        elif dist_to_player > self.aggro_radius and self.current_phase["name"] in ("Engage", "Shoot"):
            # If player runs away, go back to patrolling
            self.current_phase = self.phases[0]
            self.phase_timer = random.uniform(*self.current_phase["duration"])

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
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("NEUTRAL", 0), transparent_bg=True)
