import math
import logging

from ..data.game_constants import GLOBAL_SPEED_MULTIPLIER

def update_weapon_systems(game_state, audio_manager):
    """
    Handles weapon firing, projectile creation, and projectile movement.
    """
    # --- Weapon Cooldowns ---
    for wep_instance_id in game_state.weapon_cooldowns: 
        game_state.weapon_cooldowns[wep_instance_id] = max(0, game_state.weapon_cooldowns[wep_instance_id] - 1)

    # --- Weapon Firing ---
    game_state.active_flames.clear()
    if game_state.actions["fire"]:
        for point_name, weapon in game_state.mounted_weapons.items():
            if weapon and game_state.weapon_cooldowns[weapon.instance_id] <= 0:
                ammo_type = weapon.ammo_type
                if game_state.ammo_counts.get(ammo_type, 0) > 0:
                    point_data = game_state.attachment_points.get(point_name)
                    if not point_data: continue
                    game_state.ammo_counts[ammo_type] -= 1
                    game_state.weapon_cooldowns[weapon.instance_id] = weapon.fire_rate
                    
                    # Get the car's current angle (in game-world coordinates, where 0 is North)
                    car_angle_rad = game_state.car_angle
                    
                    # Convert to standard mathematical angle for trig functions (where 0 is East)
                    math_angle_rad = car_angle_rad - math.pi / 2
                    car_cos = math.cos(math_angle_rad)
                    car_sin = math.sin(math_angle_rad)
                    
                    # Muzzle position in car's local space
                    muzzle_local_x = point_data["offset_x"]
                    muzzle_local_y = point_data["offset_y"]
                    
                    # Rotated muzzle position
                    rotated_muzzle_x = muzzle_local_x * car_cos - muzzle_local_y * car_sin
                    rotated_muzzle_y = muzzle_local_x * car_sin + muzzle_local_y * car_cos
                    
                    # Final projectile position in world coordinates
                    p_x = game_state.car_world_x + rotated_muzzle_x
                    p_y = game_state.car_world_y + rotated_muzzle_y
                    
                    projectile_power = weapon.damage * game_state.level_damage_modifier
                    
                    for i in range(weapon.pellet_count):
                        angle_offset = 0
                        if weapon.pellet_count > 1:
                            angle_offset = (i - (weapon.pellet_count - 1) / 2) * weapon.spread_angle / (weapon.pellet_count -1)
                        
                        # Final projectile angle in game-world coordinates
                        p_angle_rad = car_angle_rad + game_state.weapon_angle_offset + angle_offset
                        
                        # Convert to mathematical angle for physics calculations
                        p_math_angle_rad = p_angle_rad - math.pi / 2

                        # All projectiles need an origin point to calculate range
                        origin_x, origin_y = p_x, p_y
                        
                        particle_char = weapon.particle
                        if "special_effect" in weapon.modifiers and weapon.modifiers["special_effect"] == "explosive_rounds":
                            particle_char = "*"

                        if weapon.weapon_type_id == "wep_flamethrower":
                            end_x = p_x + weapon.range * math.cos(p_math_angle_rad)
                            end_y = p_y + weapon.range * math.sin(p_math_angle_rad)
                            game_state.active_flames.append([p_x, p_y, end_x, end_y, projectile_power])
                            audio_manager.play_sfx("flamethrower")
                        else:
                            game_state.active_particles.append([
                                p_x, p_y, 
                                p_math_angle_rad, 
                                weapon.speed * GLOBAL_SPEED_MULTIPLIER, 
                                projectile_power, 
                                weapon.range, 
                                particle_char,
                                origin_x,
                                origin_y
                            ])
                            audio_manager.play_sfx(weapon.weapon_type_id)
