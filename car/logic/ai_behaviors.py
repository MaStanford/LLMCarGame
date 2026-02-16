import math
import random
from ..entities.obstacles.mine import Mine
from ..data.game_constants import GLOBAL_SPEED_MULTIPLIER

# --- Enemy projectile constants ---
ENEMY_PROJECTILE_SPEED = 4.0 * GLOBAL_SPEED_MULTIPLIER
ENEMY_PROJECTILE_RANGE = 150
ENEMY_PROJECTILE_CHAR = "·"
ENEMY_SHOOT_COOLDOWN = 1.5  # seconds between shots
ENEMY_SNIPE_COOLDOWN = 2.0


BEHAVIOR_COSTS = {
    "RAM": 3,
    "STRAFE": 2, "FLANK": 2,
    "CHASE": 1, "SHOOT": 1, "SNIPE": 1, "DEPLOY_MINE": 1,
    "EVADE": 0, "PATROL": 0, "STATIONARY": 0, "IDLE": 0,
}


def _get_aim_spread(game_state):
    """Returns the difficulty-scaled aim spread multiplier."""
    return game_state.difficulty_mods.get("enemy_aim_spread", 1.0)


def _get_movement_jitter(game_state):
    """Returns the difficulty-scaled movement jitter factor (0 = perfect, 1 = wild)."""
    return game_state.difficulty_mods.get("enemy_movement_jitter", 0.1)


def _fire_enemy_projectile(enemy, game_state, damage, accuracy=0.15):
    """Create an enemy projectile aimed at the player with difficulty-scaled spread."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    angle = math.atan2(dy, dx)
    # Scale accuracy spread by difficulty
    scaled_accuracy = accuracy * _get_aim_spread(game_state)
    angle += random.uniform(-scaled_accuracy, scaled_accuracy)

    # Scale damage by difficulty
    dmg_mult = game_state.difficulty_mods.get("enemy_dmg_mult", 1.0)
    scaled_damage = max(1, int(damage * dmg_mult))

    game_state.active_particles.append([
        enemy.x + enemy.width / 2,
        enemy.y + enemy.height / 2,
        angle,
        ENEMY_PROJECTILE_SPEED,
        scaled_damage,
        ENEMY_PROJECTILE_RANGE,
        ENEMY_PROJECTILE_CHAR,
        enemy.x,
        enemy.y,
        "enemy"
    ])


def _try_shoot(enemy, game_state, cooldown, damage, accuracy=0.15):
    """Attempt to fire if cooldown has elapsed. Returns True if fired."""
    last_shot = enemy.ai_state.get("last_shot_time", 0)
    now = enemy.ai_state.get("elapsed", 0)
    if now - last_shot >= cooldown:
        _fire_enemy_projectile(enemy, game_state, damage, accuracy)
        enemy.ai_state["last_shot_time"] = now
        return True
    return False


def _execute_chase_behavior(enemy, game_state, edata):
    """Moves the enemy towards the player with difficulty-scaled steering jitter."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        jitter = _get_movement_jitter(game_state)
        enemy.vx = (dx / dist + random.uniform(-jitter, jitter)) * edata.speed
        enemy.vy = (dy / dist + random.uniform(-jitter, jitter)) * edata.speed

def _execute_strafe_behavior(enemy, game_state, edata):
    """Circles the player at a distance."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        # Move perpendicular to the player
        enemy.vx = -dy / dist * edata.speed
        enemy.vy = dx / dist * edata.speed

def _execute_ram_behavior(enemy, game_state, edata):
    """Moves aggressively towards the player with a speed boost and difficulty-scaled jitter."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        jitter = _get_movement_jitter(game_state)
        enemy.vx = (dx / dist + random.uniform(-jitter, jitter)) * edata.speed * 1.5
        enemy.vy = (dy / dist + random.uniform(-jitter, jitter)) * edata.speed * 1.5

def _execute_evade_behavior(enemy, game_state, edata):
    """Moves away from the player with difficulty-scaled steering jitter."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        jitter = _get_movement_jitter(game_state)
        enemy.vx = -(dx / dist + random.uniform(-jitter, jitter)) * edata.speed
        enemy.vy = -(dy / dist + random.uniform(-jitter, jitter)) * edata.speed

def _execute_stationary_behavior(enemy, game_state, edata):
    """Stops the enemy's movement."""
    enemy.vx = 0
    enemy.vy = 0

def _execute_patrol_behavior(enemy, game_state, edata):
    """
    Moves the entity towards its patrol target.
    If the target is reached, a new one is generated.
    """
    if enemy.patrol_target_x is None:
        enemy.patrol_target_x = enemy.x + random.uniform(-100, 100)
        enemy.patrol_target_y = enemy.y + random.uniform(-100, 100)

    dist_to_target_sq = (enemy.x - enemy.patrol_target_x)**2 + (enemy.y - enemy.patrol_target_y)**2
    if dist_to_target_sq < 25:
        enemy.patrol_target_x = enemy.x + random.uniform(-100, 100)
        enemy.patrol_target_y = enemy.y + random.uniform(-100, 100)

    dx = enemy.patrol_target_x - enemy.x
    dy = enemy.patrol_target_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        enemy.vx = (dx / dist) * edata.speed * 0.5
        enemy.vy = (dy / dist) * edata.speed * 0.5


def _execute_deploy_mine_behavior(enemy, game_state, edata):
    """Flees from the player and deploys a mine."""
    if "mine_cooldown" not in enemy.ai_state:
        enemy.ai_state["mine_cooldown"] = 0

    if enemy.ai_state["mine_cooldown"] > 0:
        enemy.ai_state["mine_cooldown"] -= 1
        _execute_chase_behavior(enemy, game_state, edata)
        return

    # Flee from the player
    dx = enemy.x - game_state.car_world_x
    dy = enemy.y - game_state.car_world_y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        enemy.vx = (dx / dist) * edata.speed
        enemy.vy = (dy / dist) * edata.speed

    # Deploy a mine if far enough away
    dist_sq = (enemy.x - game_state.car_world_x)**2 + (enemy.y - game_state.car_world_y)**2
    if dist_sq > 100:
        new_mine = Mine(enemy.x, enemy.y)
        game_state.active_obstacles.append(new_mine)
        enemy.ai_state["mine_cooldown"] = 150  # 5 seconds cooldown


# --- New shooting behaviors ---

def _execute_shoot_behavior(enemy, game_state, edata):
    """Face player, maintain medium distance (80-120), fire periodically."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)

    # Maintain distance: approach if too far, retreat if too close
    preferred_dist = 100
    if dist > 0:
        if dist > preferred_dist + 20:
            # Close in
            enemy.vx = (dx / dist) * edata.speed * 0.7
            enemy.vy = (dy / dist) * edata.speed * 0.7
        elif dist < preferred_dist - 20:
            # Back off
            enemy.vx = -(dx / dist) * edata.speed * 0.5
            enemy.vy = -(dy / dist) * edata.speed * 0.5
        else:
            # Drift sideways slowly
            enemy.vx = -dy / dist * edata.speed * 0.3
            enemy.vy = dx / dist * edata.speed * 0.3

    shoot_damage = getattr(edata, 'shoot_damage', 3)
    _try_shoot(enemy, game_state, ENEMY_SHOOT_COOLDOWN, shoot_damage, accuracy=0.15)


def _execute_snipe_behavior(enemy, game_state, edata):
    """Hold position at long range, fire accurate shots."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)

    preferred_dist = 160
    if dist > 0:
        if dist > preferred_dist + 30:
            enemy.vx = (dx / dist) * edata.speed * 0.5
            enemy.vy = (dy / dist) * edata.speed * 0.5
        elif dist < preferred_dist - 30:
            enemy.vx = -(dx / dist) * edata.speed * 0.6
            enemy.vy = -(dy / dist) * edata.speed * 0.6
        else:
            # Nearly stationary
            enemy.vx *= 0.8
            enemy.vy *= 0.8

    shoot_damage = getattr(edata, 'shoot_damage', 4)
    _try_shoot(enemy, game_state, ENEMY_SNIPE_COOLDOWN, shoot_damage, accuracy=0.08)


def _execute_flank_behavior(enemy, game_state, edata):
    """Circle to player's side/rear, then shoot, with difficulty-scaled jitter."""
    dx = game_state.car_world_x - enemy.x
    dy = game_state.car_world_y - enemy.y
    dist = math.sqrt(dx*dx + dy*dy)

    if dist > 0:
        jitter = _get_movement_jitter(game_state)
        # Strong perpendicular movement + slight approach
        perp_x = -dy / dist
        perp_y = dx / dist
        approach_x = dx / dist
        approach_y = dy / dist

        if dist > 130:
            # Close in more while flanking
            enemy.vx = (perp_x * 0.6 + approach_x * 0.4 + random.uniform(-jitter, jitter)) * edata.speed
            enemy.vy = (perp_y * 0.6 + approach_y * 0.4 + random.uniform(-jitter, jitter)) * edata.speed
        elif dist < 60:
            # Too close, pull away while circling
            enemy.vx = (perp_x * 0.7 - approach_x * 0.3 + random.uniform(-jitter, jitter)) * edata.speed
            enemy.vy = (perp_y * 0.7 - approach_y * 0.3 + random.uniform(-jitter, jitter)) * edata.speed
        else:
            # Circle at good range
            enemy.vx = (perp_x + random.uniform(-jitter, jitter)) * edata.speed
            enemy.vy = (perp_y + random.uniform(-jitter, jitter)) * edata.speed

    shoot_damage = getattr(edata, 'shoot_damage', 3)
    _try_shoot(enemy, game_state, ENEMY_SHOOT_COOLDOWN, shoot_damage, accuracy=0.2)


def _execute_idle_behavior(enemy, game_state, edata):
    """Decelerate and drift. Gives the player breathing room."""
    enemy.vx *= 0.9
    enemy.vy *= 0.9


# --- Behavior dispatch map ---
BEHAVIOR_MAP = {
    "CHASE": _execute_chase_behavior,
    "STRAFE": _execute_strafe_behavior,
    "RAM": _execute_ram_behavior,
    "EVADE": _execute_evade_behavior,
    "STATIONARY": _execute_stationary_behavior,
    "PATROL": _execute_patrol_behavior,
    "DEPLOY_MINE": _execute_deploy_mine_behavior,
    "SHOOT": _execute_shoot_behavior,
    "SNIPE": _execute_snipe_behavior,
    "FLANK": _execute_flank_behavior,
    "IDLE": _execute_idle_behavior,
}


def execute_behavior(behavior_name, enemy, game_state, edata):
    """Look up and execute a behavior by name."""
    fn = BEHAVIOR_MAP.get(behavior_name)
    if fn:
        fn(enemy, game_state, edata)
