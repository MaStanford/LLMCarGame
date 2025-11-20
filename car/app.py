from textual.app import App
from textual.reactive import reactive
from textual.events import Key
import logging
from .screens.world import WorldScreen
from .screens.main_menu import MainMenuScreen
from .screens.pause_menu import PauseScreen
from .screens.inventory import InventoryScreen
from .screens.shop import ShopScreen
from .screens.city_hall import CityHallScreen
from .screens.game_over import GameOverScreen
from .screens.map import MapScreen
from .game_state import GameState
from .world import World
from .logic.spawning import spawn_enemy, spawn_fauna, spawn_obstacle
from .logic.physics import update_physics_and_collisions
from .logic.quest_logic import update_quests
from .audio.audio import AudioManager
from .data.game_constants import CUTSCENE_RADIUS
from .widgets.entity_modal import EntityModal
from .widgets.explosion import Explosion
from .widgets.notifications import Notifications
from .widgets.fps_counter import FPSCounter
from .world.generation import get_buildings_in_city
from .data import factions as faction_data_module
from .config import load_settings
import random
import math
import time
import importlib
from . import data as game_data

class GenesisModuleApp(App):
    """The main application class for the Genesis Module RPG."""

    CSS_PATH = "app.css"
    
    llm_pipeline = reactive(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Game state will be initialized upon starting a new game
        self.game_state = None
        self.world = None
        self.audio_manager = AudioManager()
        self.frame_count = 0
        self.last_update_time = time.time()
        self.game_loop = None
        self.dev_mode = False
        self.data = game_data
        self.settings = load_settings()
        self.generation_mode = self.settings.get("generation_mode", "local")

    def reload_dynamic_data(self):
        """Forces a reload of the data modules to pick up generated content."""
        try:
            # We no longer need to reload the faction module this way
            # importlib.reload(faction_data_module)
            importlib.reload(self.data)
            logging.info("Dynamic game data reloaded successfully.")
        except Exception as e:
            logging.error(f"Failed to reload dynamic data: {e}", exc_info=True)

    def stop_game_loop(self):
        """Stops the game loop timer."""
        if self.game_loop:
            self.game_loop.stop()

    def start_game_loop(self):
        """Starts the game loop timer."""
        # Ensure any old timer is stopped before creating a new one.
        if self.game_loop:
            self.game_loop.stop()
        self.game_loop = self.set_interval(1 / 30, self.update_game)

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.push_screen(MainMenuScreen())

    def switch_screen(self, screen) -> None:
        """Switch to a new screen."""
        if screen == "main_menu":
            super().switch_screen(MainMenuScreen())
        else:
            super().switch_screen(screen)



    def update_game(self) -> None:
        """The main game loop, called by a timer."""
        if not isinstance(self.screen, WorldScreen):
            return
        
        gs = self.game_state
        
        # --- Delta Time Calculation ---
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        # Decrement cooldowns
        if gs.menu_nav_cooldown > 0:
            gs.menu_nav_cooldown -= 1
        
        if not gs.pause_menu_open and not gs.menu_open:
            if gs.game_over:
                self.stop_game_loop()
                self.push_screen(GameOverScreen())
                return

            notifications = update_physics_and_collisions(gs, self.world, self.audio_manager, dt)
            for notification in notifications:
                self.screen.query_one("#notifications", Notifications).add_notification(notification)

            # Spawning logic
            gs.enemy_spawn_timer -= dt
            if gs.enemy_spawn_timer <= 0:
                spawn_enemy(gs, self.world)
                gs.enemy_spawn_timer = random.uniform(1.5, 3.5) # Spawn every 1.5-3.5 seconds

            gs.fauna_spawn_timer -= dt
            if gs.fauna_spawn_timer <= 0:
                spawn_fauna(gs, self.world)
                gs.fauna_spawn_timer = random.uniform(2.0, 4.0)

            gs.obstacle_spawn_timer -= dt
            if gs.obstacle_spawn_timer <= 0:
                spawn_obstacle(gs, self.world)
                gs.obstacle_spawn_timer = random.uniform(1.0, 2.5)
            
            quest_notifications = update_quests(gs, self.audio_manager, self)
            for notification in quest_notifications:
                self.screen.query_one("#notifications", Notifications).add_notification(notification)

            # --- Throttled UI Updates ---
            # These calculations are expensive, so we only run them a few times per second.
            if self.frame_count % 8 == 0:
                gs.closest_entity_info = self.find_closest_entity()
            
            if self.frame_count % 12 == 0:
                self.update_compass_data()

            # --- Proximity Quest Generation ---
            if self.frame_count % 90 == 0: # Every 3 seconds
                self.check_and_cache_quests_for_nearby_cities()

            # --- Update UI Widgets ---
            self.screen.update_widgets()

            # Check for building interactions
            self.check_building_interaction()

            # --- Reset one-time actions ---
            gs.actions["fire"] = False

        # Update FPS counter
        self.frame_count += 1
        if isinstance(self.screen, WorldScreen):
            # Use a simple moving average for FPS to smooth it out
            # This part of the code is for display only and doesn't affect game logic timing
            if current_time - self.screen.query_one("#fps_counter").last_fps_update_time >= 1.0:
                fps = self.frame_count / (current_time - self.screen.query_one("#fps_counter").last_fps_update_time)
                self.screen.query_one("#fps_counter").fps = fps
                self.screen.query_one("#fps_counter").last_fps_update_time = current_time
                self.frame_count = 0

    def check_building_interaction(self):
        """Checks if the player is inside a building and pushes the appropriate screen."""
        gs = self.game_state
        buildings = get_buildings_in_city(round(gs.car_world_x / 1000), round(gs.car_world_y / 1000))
        for building in buildings:
            if (building['x'] <= gs.car_world_x < building['x'] + building['w'] and
                building['y'] <= gs.car_world_y < building['y'] + building['h']):
                
                building_type = building.get("type")
                if building_type in ["mechanic_shop", "gas_station", "weapon_shop"]:
                    gs.menu_open = True
                    self.push_screen(ShopScreen(shop_type=building_type))
                elif building_type == 'city_hall':
                    gs.menu_open = True
                    self.push_screen(CityHallScreen())
                return

    def find_closest_entity(self):
        """Finds the closest enemy or boss to the player."""
        gs = self.game_state
        closest = None
        min_dist_sq = CUTSCENE_RADIUS**2

        # Prioritize finding the closest faction boss
        for enemy in gs.active_enemies:
            if getattr(enemy, "is_faction_boss", False):
                dist_sq = (enemy.x - gs.car_world_x)**2 + (enemy.y - gs.car_world_y)**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    art = enemy.art.get("N") if isinstance(enemy.art, dict) else enemy.art
                    closest = {
                        "name": enemy.name, "hp": enemy.durability, "max_hp": enemy.max_durability,
                        "art": art
                    }
        
        # If no boss is nearby, find the closest normal enemy
        if not closest:
            for enemy in gs.active_enemies:
                dist_sq = (enemy.x - gs.car_world_x)**2 + (enemy.y - gs.car_world_y)**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    art = enemy.art.get("N") if isinstance(enemy.art, dict) else enemy.art
                    closest = {
                        "name": enemy.__class__.__name__.replace("_", " ").title(),
                        "hp": enemy.durability, "max_hp": enemy.max_durability,
                        "art": art
                    }
        return closest

    def update_compass_data(self):
        """Calculates the compass direction and caches it in the game state."""
        gs = self.game_state
        target_x, target_y, target_name = None, None, None
        
        if gs.waypoint:
            target_x, target_y = gs.waypoint
            target_name = "Waypoint"
        elif gs.current_quest:
            if gs.current_quest.ready_to_turn_in:
                target_x = gs.current_quest.city_id[0] * CITY_SPACING
                target_y = gs.current_quest.city_id[1] * CITY_SPACING
                target_name = "Turn In Quest"
            elif gs.current_quest.boss:
                boss = gs.current_quest.boss
                target_x, target_y = boss.x, boss.y
                target_name = boss.name
        
        if target_x is not None:
            angle_to_target = math.atan2(target_y - gs.car_world_y, target_x - gs.car_world_x)
            gs.compass_info = {
                "target_angle": math.degrees(angle_to_target),
                "player_angle": gs.car_angle,
                "target_name": target_name
            }
        else:
            gs.compass_info = {"target_angle": 0, "player_angle": 0, "target_name": ""}

    def on_worker_state_changed(self, event: "Worker.StateChanged") -> None:
        """Handles completed quest generation workers."""
        if event.worker.name.startswith("QuestGenerator"):
            if event.worker.state == "SUCCESS":
                city_id = event.worker.city_id
                quests = event.worker.result
                if quests:
                    self.game_state.quest_cache[city_id] = quests
                    logging.info(f"Successfully cached {len(quests)} quests for city {city_id}.")
                else:
                    self.game_state.quest_cache.pop(city_id, None)
                    logging.warning(f"Quest generation failed for city {city_id}. No quests cached.")
                
                from .screens.city_hall import CityHallScreen, QuestsLoaded
                if isinstance(self.screen, CityHallScreen) and self.screen.current_city_id == city_id:
                    logging.info(f"Posting QuestsLoaded message to CityHallScreen for city {city_id}")
                    self.screen.post_message(QuestsLoaded(quests or []))

    def trigger_initial_quest_cache(self):
        """Kicks off the quest caching for the player's starting area."""
        self.check_and_cache_quests_for_nearby_cities()

    def check_and_cache_quests_for_nearby_cities(self):
        """
        Checks for cities near the player and dispatches workers to generate quests
        for them if they aren't already cached.
        """
        from .workers.quest_generator import generate_quests_worker
        from .world.generation import get_city_faction
        from functools import partial

        gs = self.game_state
        player_grid_x = round(gs.car_world_x / 1000)
        player_grid_y = round(gs.car_world_y / 1000)

        # Check a 3x3 grid around the player
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                check_x, check_y = player_grid_x + dx, player_grid_y + dy
                city_id = f"city_{check_x}_{check_y}"

                # Don't generate quests for cities that are already cached or pending
                if city_id in gs.quest_cache:
                    continue

                # Mark as pending to prevent re-dispatching
                gs.quest_cache[city_id] = "pending"

                city_faction_id = get_city_faction(check_x * 1000, check_y * 1000, gs.factions)
                
                logging.info(f"No quests cached for nearby city {city_id}. Starting pre-fetch worker.")

                worker_callable = partial(
                    generate_quests_worker,
                    app=self,
                    city_id=city_id,
                    city_faction_id=city_faction_id,
                    theme=gs.theme,
                    faction_data=gs.factions,
                    story_intro=gs.story_intro
                )
                
                worker = self.run_worker(
                    worker_callable,
                    exclusive=False, # Allow multiple quest generators to run
                    thread=True,
                    name=f"QuestGenerator_{city_id}"
                )
                # Pass the city_id to the worker's custom attribute to know where to store the result
                worker.city_id = city_id

    def trigger_initial_quest_cache(self):
        """Kicks off the quest caching for the player's starting area."""
        self.check_and_cache_quests_for_nearby_cities()
