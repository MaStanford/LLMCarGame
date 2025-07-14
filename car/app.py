from textual.app import App
from .screens.default import DefaultScreen
from .screens.main_menu import MainMenuScreen
from .screens.pause_menu import PauseScreen
from .screens.inventory import InventoryScreen
from .screens.shop import ShopScreen
from .screens.city_hall import CityHallScreen
from .game_state import GameState
from .world import World
from .logic.spawning import spawn_enemy, spawn_fauna, spawn_obstacle
from .logic.physics import update_physics_and_collisions
from .logic.quest_logic import update_quests
from .audio.audio import AudioManager
from .data.game_constants import CUTSCENE_RADIUS
from .widgets.hud import HUD
from .widgets.entity_modal import EntityModal
from .widgets.explosion import Explosion
from .world.generation import get_buildings_in_city
import random
import math

class CarApp(App):
    """The main application class for the Car RPG."""

    CSS_PATH = "app.css"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Game state will be initialized upon starting a new game
        self.game_state = None
        self.world = None
        self.audio_manager = AudioManager()

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.push_screen(MainMenuScreen())

    def action_push_screen(self, screen: str) -> None:
        """Action to push a screen."""
        if screen == "pause_menu":
            self.push_screen(PauseScreen())
        elif screen == "inventory":
            self.push_screen(InventoryScreen())



    def update_game(self) -> None:
        """The main game loop, called by a timer."""
        if not isinstance(self.screen, DefaultScreen):
            return
        gs = self.game_state
        # Decrement cooldowns
        if gs.menu_nav_cooldown > 0:
            gs.menu_nav_cooldown -= 1
        
        if not gs.pause_menu_open and not gs.menu_open:
            # Player actions are now handled by the on_key event in DefaultScreen
            notifications = update_physics_and_collisions(gs, self.world, self.audio_manager)
            for notification in notifications:
                self.screen.query_one("#notifications", Notifications).add_notification(notification)

            # Spawning logic
            gs.enemy_spawn_timer -= 1
            if gs.enemy_spawn_timer <= 0:
                spawn_enemy(gs, self.world)
                gs.enemy_spawn_timer = random.randint(50, 100)

            gs.fauna_spawn_timer -= 1
            if gs.fauna_spawn_timer <= 0:
                spawn_fauna(gs, self.world)
                gs.fauna_spawn_timer = random.randint(50, 100)

            gs.obstacle_spawn_timer -= 1
            if gs.obstacle_spawn_timer <= 0:
                spawn_obstacle(gs, self.world)
                gs.obstacle_spawn_timer = random.randint(50, 100)
            
            quest_notifications = update_quests(gs, self.audio_manager)
            for notification in quest_notifications:
                self.screen.query_one("#notifications", Notifications).add_notification(notification)

            # Check for building interactions
            self.check_building_interaction()

        # --- Update UI Widgets ---
        self.screen.frame_update(gs)

    def check_building_interaction(self):
        """Checks if the player is inside a building and pushes the appropriate screen."""
        gs = self.game_state
        buildings = get_buildings_in_city(round(gs.car_world_x / 1000), round(gs.car_world_y / 1000))
        for building in buildings:
            if (building['x'] <= gs.car_world_x < building['x'] + building['w'] and
                building['y'] <= gs.car_world_y < building['y'] + building['h']):
                if building['type'] == 'shop':
                    self.push_screen(ShopScreen())
                elif building['type'] == 'city_hall':
                    self.push_screen(CityHallScreen())
                return

    def find_closest_entity(self):
        """Finds the closest enemy or boss to the player."""
        gs = self.game_state
        closest = None
        min_dist_sq = CUTSCENE_RADIUS**2

        for boss in gs.active_bosses.values():
            dist_sq = (boss.x - gs.car_world_x)**2 + (boss.y - gs.car_world_y)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest = {
                    "name": boss.name, "hp": boss.hp, "max_hp": boss.max_durability,
                    "art": boss.art.get("N", [])
                }
        
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



