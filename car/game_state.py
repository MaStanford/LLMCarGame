import math
import random
import importlib
from .entities.weapon import Weapon
from .logic.entity_loader import PLAYER_CARS
from .data import *

class GameState:
    def __init__(self, selected_car_index, difficulty, difficulty_mods, car_color_names, car_color_pair_num, player_cash=300):
        # --- Game Configuration ---
        self.selected_car_index = selected_car_index
        self.difficulty = difficulty
        self.difficulty_mods = difficulty_mods
        self.car_color_names = car_color_names
        self.car_color_pair_num = car_color_pair_num
        
        # --- Player State ---
        self.player_cash = player_cash
        
        # --- Player Car ---
        car_class = PLAYER_CARS[self.selected_car_index]
        self.player_car = car_class(0, 0)
        self.all_entities = [self.player_car]

        # --- Base Stats for Leveling ---
        self.base_max_durability = self.player_car.durability
        self.base_gas_capacity = self.player_car.fuel
        # These need to be added to the car classes
        self.base_horsepower = self.player_car.speed * 10
        self.base_turn_rate = self.player_car.handling
        self.base_braking_power = self.player_car.braking_power

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
        self.xp_to_next_level = 100 # Placeholder
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
        self.player_inventory = []
        self.mounted_weapons = {
            mount_point: Weapon(weapon_type_id, instance_id=f"{weapon_type_id}_default") 
            for mount_point, weapon_type_id in self.player_car.default_weapons.items()
        }
        self.attachment_points = self.player_car.attachment_points
        self.ammo_counts = {}
        self.weapon_cooldowns = {}

        for weapon in self.mounted_weapons.values():
            if weapon:
                self.weapon_cooldowns[weapon.instance_id] = 0
                ammo_type = weapon.ammo_type
                if ammo_type not in self.ammo_counts:
                    self.ammo_counts[ammo_type] = 0
                self.ammo_counts[ammo_type] += 100 # Starting ammo


        # --- Derived Stats ---
        self.acceleration_factor = 0.0
        self.braking_deceleration_factor = 0.0
        self.max_speed = 0.0
        self.gas_consumption_scaler = 0.01
        self.drag_coefficient = 0.01 # Placeholder
        self.gas_consumption_rate = 0.1 # Placeholder

        # --- World and Entity State ---
        self.active_obstacles = {}
        self.next_obstacle_id = 0
        self.obstacle_spawn_timer = 0
        self.active_particles = []
        self.active_flames = []
        self.active_pickups = {}
        self.next_pickup_id = 0
        self.active_fauna = []
        self.fauna_spawn_timer = 0
        self.active_bosses = {}
        self.active_enemies = []
        self.enemy_spawn_timer = 0
        
        # --- Quest State ---
        self.current_quest = None
        self.town_reputation = {}

        # --- UI and Game Flow State ---
        self.shop_cooldown = 0
        self.menu_toggle_cooldown = 0
        self.game_over = False
        self.game_over_message = ""
        self.menu_open = False
        self.play_again = False
        self.frame = 0
        self.menu_selected_section_idx = 0
        self.menu_selected_item_idx = 0
        self.menu_preview_angle = 0.0
        self.spawn_radius = 0
        self.despawn_radius = 0
        self.screen_width = 0
        self.screen_height = 0
        self.notifications = []

        self.apply_level_bonuses()

    def gain_xp(self, xp):
        self.current_xp += xp
        while self.current_xp >= self.xp_to_next_level:
            if self.player_level < 100: # Placeholder max level
                self.current_xp -= self.xp_to_next_level
                self.player_level += 1
                self.xp_to_next_level = int(self.xp_to_next_level * 1.5) # Placeholder
                self.apply_level_bonuses()
                self.level_up_message_timer = 60
            else:
                self.current_xp = self.xp_to_next_level
                break

    def apply_level_bonuses(self):
        level_bonus_multiplier = 1.0 + (self.player_level - 1) * 0.1 # Placeholder

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
