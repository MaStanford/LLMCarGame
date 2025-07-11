import math
import logging

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
                    
                    # Adjust angle for world coordinates
                    adjusted_angle = game_state.car_angle
                    car_cos = math.cos(adjusted_angle)
                    car_sin = math.sin(adjusted_angle)
                    
                    # Muzzle position in car's local space
                    muzzle_local_x = point_data["offset_x"]
                    muzzle_local_y = point_data["offset_y"]
                    
                    # Rotated muzzle position
                    rotated_muzzle_x = muzzle_local_x * car_cos - muzzle_local_y * car_sin
                    rotated_muzzle_y = muzzle_local_x * car_sin + muzzle_local_y * car_cos
                    
                    # Final projectile position in world coordinates
                    # This logic mirrors the renderer's screen coordinate calculation
                    p_x = game_state.car_world_x + rotated_muzzle_x
                    p_y = game_state.car_world_y + rotated_muzzle_y
                    
                    projectile_power = weapon.damage * game_state.level_damage_modifier
                    
                    for i in range(weapon.pellet_count):
                        angle_offset = 0
                        if weapon.pellet_count > 1:
                            angle_offset = (i - (weapon.pellet_count - 1) / 2) * weapon.spread_angle / (weapon.pellet_count -1)
                        
                        p_angle = adjusted_angle + angle_offset
                        corrected_p_angle = p_angle - math.pi / 2

                        if "special_effect" in weapon.modifiers and weapon.modifiers["special_effect"] == "explosive_rounds":
                            game_state.active_particles.append([p_x, p_y, corrected_p_angle, weapon.speed, projectile_power, weapon.range, "*"])
                        elif weapon.weapon_type_id == "wep_flamethrower":
                            end_x = p_x + weapon.range * math.cos(corrected_p_angle)
                            end_y = p_y + weapon.range * math.sin(corrected_p_angle)
                            game_state.active_flames.append([p_x, p_y, end_x, end_y, projectile_power])
                            audio_manager.play_sfx("flamethrower")
                        else:
                            game_state.active_particles.append([p_x, p_y, corrected_p_angle, weapon.speed, projectile_power, weapon.range, weapon.particle])
                            audio_manager.play_sfx(weapon.weapon_type_id)
