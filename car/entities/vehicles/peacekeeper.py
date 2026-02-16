from ..vehicle import Vehicle

from ...data.game_constants import GLOBAL_SPEED_MULTIPLIER

class Peacekeeper(Vehicle):
    """
    A standard patrol vehicle from The Junction.
    It patrols a set area and gives chase only when provoked.
    """
    def __init__(self, x, y):
        art = {
            # North (Facing Up) - hood at top, trunk at bottom
            "N": [
                " ▄▓▄ ",
                "●░░░●",
                "█▓▓▓█",
                "●███●",
                " ▀█▀ "
            ],
            # South (Facing Down) - vertical mirror of N
            "S": [
                " ▄█▄ ",
                "●███●",
                "█▓▓▓█",
                "●░░░●",
                " ▀▓▀ "
            ],
            # East (Facing Right) - hood on right, sleek profile
            "E": [
                "●▓██░▓▄ ",
                "█▓██▓░░▌",
                "●▓██░▓▀ "
            ],
            # West (Facing Left) - horizontal mirror of E
            "W": [
                " ▄▓░██▓●",
                "▐░░▓██▓█",
                " ▀▓░██▓●"
            ],
            # North-East - front at upper-right
            "NE": [
                "  ▄░▓▄",
                " ●█░▓█",
                "▐█▓██●",
                " ▀█▀  "
            ],
            # North-West - horizontal mirror of NE
            "NW": [
                "▄▓░▄  ",
                "█▓░█● ",
                "●██▓█▌",
                "  ▀█▀ "
            ],
            # South-East - vertical mirror of NE
            "SE": [
                " ▄█▄  ",
                "▐█▓██●",
                " ●█░▓█",
                "  ▀░▓▀"
            ],
            # South-West - horizontal mirror of SE
            "SW": [
                "  ▄█▄ ",
                "●██▓█▌",
                "█▓░█● ",
                "▀▓░▀  "
            ]
        }
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

    def update(self, game_state, world, dt):
        import random
        from ...logic.ai_behaviors import execute_behavior

        dist_to_player = ((self.x - game_state.car_world_x)**2 + (self.y - game_state.car_world_y)**2)**0.5

        # If player runs away during combat, go back to patrolling
        if dist_to_player > self.aggro_radius and self.current_phase["name"] in ("Engage", "Shoot"):
            self.current_phase = self.phases[0]
            self.phase_timer = random.uniform(*self.current_phase["duration"])

        # Patrol phase handled manually (no budget needed)
        if self.current_phase["name"] == "Patrol":
            self.ai_state["elapsed"] = self.ai_state.get("elapsed", 0) + dt
            self.phase_timer -= dt
            if dist_to_player <= self.aggro_radius:
                self.current_phase = next((p for p in self.phases if p["name"] == "Engage"), self.phases[1])
                self.phase_timer = random.uniform(*self.current_phase["duration"])
            elif self.phase_timer <= 0:
                self.phase_timer = random.uniform(*self.current_phase["duration"])
        else:
            # Combat phases use budget-aware transitions
            self._advance_phase(game_state, dt)

        execute_behavior(self.current_phase["behavior"], self, game_state, self)

        self._move_with_terrain_check(world, dt)

    def draw(self, stdscr, game_state, world_start_x, world_start_y, color_map):
        from ...rendering.draw_utils import draw_sprite
        draw_sprite(stdscr, self.y - world_start_y, self.x - world_start_x, self.art, color_map.get("NEUTRAL", 0), transparent_bg=True)
