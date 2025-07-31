import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_patrol_behavior, _execute_chase_behavior

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
        self.phases = [
            {"name": "Patrol", "duration": (5, 8), "behavior": "PATROL", "next_phases": {"Patrol": 1.0}},
            {"name": "Engage", "duration": (10, 10), "behavior": "CHASE", "next_phases": {"Patrol": 1.0}}
        ]
        self._initialize_ai()
        self.aggro_radius = 25

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world, dt):
        self.phase_timer -= dt

        dist_to_player = ((self.x - game_state.car_world_x)**2 + (self.y - game_state.car_world_y)**2)**0.5

        if dist_to_player <= self.aggro_radius and self.current_phase["name"] == "Patrol":
            # If player gets too close, engage
            self.current_phase = self.phases[1]
            self.phase_timer = random.uniform(*self.current_phase["duration"])
        elif dist_to_player > self.aggro_radius and self.current_phase["name"] == "Engage":
            # If player runs away, go back to patrolling
            self.current_phase = self.phases[0]
            self.phase_timer = random.uniform(*self.current_phase["duration"])
        
        if self.phase_timer <= 0:
            # If timer runs out while patrolling, just reset it
             self.phase_timer = random.uniform(*self.current_phase["duration"])


        behavior = self.current_phase["behavior"]
        if behavior == "PATROL":
            _execute_patrol_behavior(self, game_state, self)
        elif behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("NEUTRAL", 0), transparent_bg=True)
