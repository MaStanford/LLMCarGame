import math
import random
from .base import Entity
from ..logic.ai_behaviors import (
    _are_factions_hostile, _get_aim_spread,
    ENEMY_PROJECTILE_SPEED, ENEMY_PROJECTILE_RANGE, ENEMY_PROJECTILE_CHAR,
)

TURRET_FIRE_RATE = 1.5  # seconds between shots
TURRET_RANGE = 120
TURRET_DAMAGE = 5
TURRET_ACCURACY = 0.12


class Turret(Entity):
    def __init__(self, x, y):
        art = [
            " ╦ ",
            "╠█╣",
            " ╩ ",
        ]
        super().__init__(x, y, art, durability=100)
        self.width = 3
        self.height = 3
        self.weight = 5000
        self.collision_damage = 3
        self.shoot_damage = TURRET_DAMAGE
        self.xp_value = 30
        self.cash_value = 25
        self.name = "Defense Turret"
        self.fire_cooldown = 0.0

    def update(self, game_state, world, dt):
        self.fire_cooldown -= dt
        if self.fire_cooldown > 0:
            return

        # Find closest hostile target within range
        target = self._find_target(game_state)
        if target is None:
            return

        tx = target[0]
        ty = target[1]
        dx = tx - (self.x + self.width / 2)
        dy = ty - (self.y + self.height / 2)
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > TURRET_RANGE:
            return

        angle = math.atan2(dy, dx)
        spread = TURRET_ACCURACY * _get_aim_spread(game_state)
        angle += random.uniform(-spread, spread)

        dmg_mult = game_state.difficulty_mods.get("enemy_dmg_mult", 1.0)
        scaled_damage = max(1, int(self.shoot_damage * dmg_mult))

        game_state.active_particles.append([
            self.x + self.width / 2,
            self.y + self.height / 2,
            angle,
            ENEMY_PROJECTILE_SPEED,
            scaled_damage,
            ENEMY_PROJECTILE_RANGE,
            ENEMY_PROJECTILE_CHAR,
            self.x,
            self.y,
            ("enemy", self.faction_id),
        ])
        self.fire_cooldown = TURRET_FIRE_RATE

    def _find_target(self, game_state):
        """Return (x, y) of the best target, or None."""
        best = None
        best_dist_sq = TURRET_RANGE * TURRET_RANGE
        my_faction = self.faction_id

        # Check player — only target if faction is hostile to the player
        player_rep = game_state.faction_reputation.get(my_faction, 0)
        if player_rep <= -50:
            px = game_state.car_world_x + game_state.player_car.width / 2
            py = game_state.car_world_y + game_state.player_car.height / 2
            d = (px - self.x) ** 2 + (py - self.y) ** 2
            if d < best_dist_sq:
                best_dist_sq = d
                best = (px, py)

        # Check rival-faction enemies
        for enemy in game_state.active_enemies:
            ef = getattr(enemy, 'faction_id', None)
            if not _are_factions_hostile(my_faction, ef, game_state):
                continue
            ex = enemy.x + enemy.width / 2
            ey = enemy.y + enemy.height / 2
            d = (ex - self.x) ** 2 + (ey - self.y) ** 2
            if d < best_dist_sq:
                best_dist_sq = d
                best = (ex, ey)

        return best
