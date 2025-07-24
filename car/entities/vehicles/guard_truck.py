import random
from ..vehicle import Vehicle
from ...logic.ai_behaviors import _execute_chase_behavior, _execute_stationary_behavior

class GuardTruck(Vehicle):
    """
    A slow but sturdy truck used by the Blue Syndicate for defensive purposes.
    It stays put until an enemy gets close, then gives a determined chase.
    """
    def __init__(self, x, y):
        art = [
            "  ▄▄▄▄▄  ",
            " ▟█████▙ ",
            "█████████",
            " (●)═(●) "
        ]
        super().__init__(x, y, art, durability=150, speed=0.4, acceleration=0.2, handling=0.2)
        self.name = "Guard Truck"
        self.xp_value = 30
        self.cash_value = 50
        self.drop_item = "ammo_bullet"
        self.drop_rate = 0.2
        self.phases = [
            {"name": "Guard", "duration": (1, 2), "behavior": "STATIONARY", "next_phases": {"Chase": 1.0}},
            {"name": "Chase", "duration": (10, 15), "behavior": "CHASE", "next_phases": {"Guard": 1.0}}
        ]
        self._initialize_ai()
        # Guard trucks only become aggressive if the player is close
        self.aggro_radius = 20

    def _initialize_ai(self):
        self.current_phase = self.phases[0]
        self.phase_timer = random.uniform(*self.current_phase["duration"])

    def update(self, game_state, world):
        self.phase_timer -= 1 / 30.0

        dist_to_player = ((self.x - game_state.car_world_x)**2 + (self.y - game_state.car_world_y)**2)**0.5
        
        # If player is far away, always stay in Guard mode
        if dist_to_player > self.aggro_radius and self.current_phase["name"] == "Chase":
            self.current_phase = self.phases[0] # Switch to Guard
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        if self.phase_timer <= 0:
            if self.current_phase["name"] == "Guard" and dist_to_player <= self.aggro_radius:
                # If guarding and player is close, switch to chase
                self.current_phase = self.phases[1]
            else:
                 # Otherwise, just switch back to guard
                self.current_phase = self.phases[0]

            self.phase_timer = random.uniform(*self.current_phase["duration"])

        behavior = self.current_phase["behavior"]
        if behavior == "CHASE":
            _execute_chase_behavior(self, game_state, self)
        elif behavior == "STATIONARY":
            _execute_stationary_behavior(self, game_state, self)

        self.x += self.vx
        self.y += self.vy

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("ENEMY_BLUE", 0), transparent_bg=True)
