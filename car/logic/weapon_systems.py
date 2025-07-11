import math

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
                    
                    car_center_world_x = game_state.car_world_x + game_state.player_car.width / 2
                    car_center_world_y = game_state.car_world_y + game_state.player_car.height / 2
                    
                    offset_x = point_data["offset_x"]
                    offset_y = point_data["offset_y"]
                    rotated_offset_x = offset_x * math.cos(game_state.car_angle) - offset_y * math.sin(game_state.car_angle)
                    rotated_offset_y = offset_x * math.sin(game_state.car_angle) + offset_y * math.cos(game_state.car_angle)
                    forward_proj_offset = game_state.player_car.width * 0.5 + 1.0
                    p_x = car_center_world_x + rotated_offset_x + forward_proj_offset * math.cos(game_state.car_angle)
                    p_y = car_center_world_y + rotated_offset_y + forward_proj_offset * math.sin(game_state.car_angle)
                    projectile_power = weapon.damage * game_state.level_damage_modifier
                    
                    for i in range(weapon.pellet_count):
                        angle_offset = 0
                        if weapon.pellet_count > 1:
                            angle_offset = (i - (weapon.pellet_count - 1) / 2) * weapon.spread_angle / (weapon.pellet_count -1)
                        
                        p_angle = game_state.car_angle + angle_offset

                        if weapon.weapon_type_id == "wep_flamethrower":
                            end_x = p_x + weapon.range * math.cos(p_angle)
                            end_y = p_y + weapon.range * math.sin(p_angle)
                            game_state.active_flames.append([p_x, p_y, end_x, end_y, projectile_power])
                            audio_manager.play_sfx("flamethrower")
                        else:
                            game_state.active_particles.append([p_x, p_y, p_angle, weapon.speed, projectile_power, weapon.range, weapon.particle])
                            audio_manager.play_sfx(weapon.weapon_type_id)
