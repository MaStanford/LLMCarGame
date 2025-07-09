import math
import random
from .data import *

class GameState:
    def __init__(self, selected_car_index, difficulty, difficulty_mods, car_color_names, car_color_pair_num):
        # --- Game Configuration ---
        self.selected_car_index = selected_car_index
        self.difficulty = difficulty
        self.difficulty_mods = difficulty_mods
        self.car_color_names = car_color_names
        self.car_color_pair_num = car_color_pair_num
        self.selected_car_data = CARS_DATA[self.selected_car_index]
        self.all_car_art = self.selected_car_data["art"]
        self.car_height, self.car_width = get_car_dimensions(self.all_car_art)

        # --- Base Stats for Leveling ---
        self.base_horsepower = self.selected_car_data["hp"]
        self.base_turn_rate = self.selected_car_data["turn_rate"]
        self.base_max_durability = self.selected_car_data["durability"]
        self.base_gas_capacity = self.selected_car_data["gas_capacity"]
        self.base_braking_power = self.selected_car_data["braking"]

        # --- Effective Stats (modified by level) ---
        self.horsepower = 0
        self.turn_rate = 0.0
        self.max_durability = 0
        self.gas_capacity = 0
        self.braking_power = 0
        self.level_damage_modifier = 1.0

        # --- XP and Level Variables ---
        self.player_level = 1
        self.current_xp = 0
        self.xp_to_next_level = INITIAL_XP_TO_LEVEL
        self.level_up_message_timer = 0

        # --- Car State ---
        self.car_world_x = 0.0
        self.car_world_y = 0.0
        self.car_angle = 0.0
        self.car_velocity_x = 0.0
        self.car_velocity_y = 0.0
        self.car_speed = 0.0
        self.current_durability = 0
        self.current_gas = 0
        self.distance_traveled = 0.0

        # --- Player State ---
        self.player_cash = 0
        self.player_inventory = list(self.selected_car_data.get("inventory", []))
        self.mounted_weapons = self.selected_car_data["mounted_weapons"]
        self.attachment_points = self.selected_car_data["attachment_points"]
        self.ammo_counts = {
            AMMO_BULLET: self.selected_car_data.get("ammo_bullet", 0),
            AMMO_HEAVY_BULLET: self.selected_car_data.get("ammo_heavy_bullet", 0),
            AMMO_FUEL: self.selected_car_data.get("ammo_fuel", 0),
        }
        self.weapon_cooldowns = {wep_key: 0 for wep_key in WEAPONS_DATA}

        # --- Derived Stats ---
        self.acceleration_factor = 0.0
        self.braking_deceleration_factor = 0.0
        self.max_speed = 0.0
        self.gas_consumption_scaler = 0.01
        self.drag_coefficient = self.selected_car_data["drag"]
        self.gas_consumption_rate = self.selected_car_data["gas_consumption"]

        # --- World and Entity State ---
        self.active_obstacles = {}
        self.next_obstacle_id = 0
        self.obstacle_spawn_timer = 0
        self.active_particles = []
        self.active_flames = []
        self.active_pickups = {}
        self.next_pickup_id = 0
        self.active_fauna = {}
        self.next_fauna_id = 0
        self.fauna_spawn_timer = 0
        self.active_bosses = {}
        self.active_enemies = {}
        self.next_enemy_id = 0
        self.enemy_spawn_timer = 0
        
        # --- Quest State ---
        self.current_quest = None

        # --- UI and Game Flow State ---
        self.shop_cooldown = 0
        self.game_over = False
        self.game_over_message = ""
        self.menu_open = False
        self.play_again = False
        self.frame = 0
        self.menu_selected_section_idx = 0
        self.menu_selected_item_idx = 0
        self.spawn_radius = 0
        self.despawn_radius = 0

        self.apply_level_bonuses()

    def gain_xp(self, xp):
        self.current_xp += xp
        while self.current_xp >= self.xp_to_next_level:
            if self.player_level < MAX_LEVEL:
                self.current_xp -= self.xp_to_next_level
                self.player_level += 1
                self.xp_to_next_level = int(self.xp_to_next_level * XP_INCREASE_PER_LEVEL_FACTOR)
                self.apply_level_bonuses()
                self.level_up_message_timer = 60
            else:
                self.current_xp = self.xp_to_next_level
                break

    def apply_level_bonuses(self):
        if self.player_level > MAX_LEVEL:
            pass

        level_bonus_multiplier = 1.0 + (self.player_level - 1) * LEVEL_STAT_BONUS_PER_LEVEL

        self.horsepower = self.base_horsepower * level_bonus_multiplier
        self.turn_rate = self.base_turn_rate * level_bonus_multiplier
        self.braking_power = self.base_braking_power * level_bonus_multiplier

        new_max_durability = int(self.base_max_durability * level_bonus_multiplier)
        durability_increase = new_max_durability - self.max_durability
        self.max_durability = new_max_durability
        self.current_durability = min(self.max_durability, self.current_durability + durability_increase)
        if self.player_level == 1:
            self.current_durability = self.max_durability

        new_gas_capacity = int(self.base_gas_capacity * level_bonus_multiplier)
        gas_increase = new_gas_capacity - self.gas_capacity
        self.gas_capacity = new_gas_capacity
        self.current_gas = min(self.gas_capacity, self.current_gas + gas_increase)
        if self.player_level == 1:
            self.current_gas = self.gas_capacity

        self.level_damage_modifier = level_bonus_multiplier

        self.acceleration_factor = self.horsepower / 500.0
        self.max_speed = self.horsepower / 4.0
        self.braking_deceleration_factor = self.braking_power / 100.0

def get_car_dimensions(car_art):
    if not car_art or not car_art[0]:
        return 0, 0
    return len(car_art[0]), len(car_art[0][0]) if car_art[0] else 0
