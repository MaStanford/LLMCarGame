import math
import logging

from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Horizontal, Vertical, Container

from ..data.game_constants import CITY_SPACING
from ..widgets.entity_modal import EntityModal
from ..widgets.explosion import Explosion
from ..widgets.hud_stats import StatsHUD
from ..widgets.hud_location import HudLocation
from ..widgets.hud_compass import CompassHUD
from ..widgets.hud_quest import QuestHUD
from ..widgets.game_view import GameView
from ..widgets.notifications import Notifications
from ..widgets.fps_counter import FPSCounter
from ..world.generation import get_city_name
from ..logic.spawning import spawn_initial_entities
from .inventory import InventoryScreen
from .pause_menu import PauseScreen
from .map import MapScreen
from .faction import FactionScreen
from .faction import FactionScreen

from textual.events import Key
from textual.binding import Binding

class WorldScreen(Screen):
    """The default screen for the game."""

    BINDINGS = [
        Binding("w", "accelerate", "Accelerate", show=True),
        Binding("s", "brake", "Brake", show=True),
        Binding("a", "turn_left", "Turn Left", show=True),
        Binding("d", "turn_right", "Turn Right", show=True),
        Binding("space", "fire", "Fire", show=True),
        Binding("escape", "toggle_pause", "Pause", show=True),
        Binding("tab", "toggle_inventory", "Inventory", show=True),
        Binding("m", "push_screen('map')", "Map", show=True),
        Binding("f", "push_screen('faction')", "Factions", show=True),
    ]

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.focus()
        gs = self.app.game_state
        
        # Synchronize the player car's entity position with the game state's world position
        gs.player_car.x = gs.car_world_x
        gs.player_car.y = gs.car_world_y
        
        # Spawn an initial batch of entities
        spawn_initial_entities(gs, self.app.world)

        # Hide FPS counter if not in dev mode
        if not self.app.dev_mode:
            self.query_one("#fps_counter").display = False

    def action_accelerate(self) -> None:
        gs = self.app.game_state
        gs.pedal_position = min(1.0, gs.pedal_position + 0.2)
    def action_brake(self) -> None:
        gs = self.app.game_state
        gs.pedal_position = max(-1.0, gs.pedal_position - 0.2)
    def action_turn_left(self) -> None:
        gs = self.app.game_state
        gs.car_angle -= gs.turn_rate
    def action_turn_right(self) -> None:
        gs = self.app.game_state
        gs.car_angle += gs.turn_rate
    def action_fire(self) -> None:
        gs = self.app.game_state
        gs.actions["fire"] = True

    def action_toggle_pause(self) -> None:
        """Toggle the pause menu."""
        if self.app.game_state.pause_menu_open:
            self.app.pop_screen()
        else:
            self.app.game_state.pause_menu_open = True
            self.app.push_screen(PauseScreen())

    def action_toggle_inventory(self) -> None:
        """Toggle the inventory screen."""
        if self.app.game_state.menu_open:
            self.app.pop_screen()
        else:
            self.app.game_state.menu_open = True
            self.app.push_screen(InventoryScreen())

    def compose(self):
        """Compose the layout of the screen."""
        yield GameView(id="game_view", game_state=self.app.game_state, world=self.app.world)
        
        with Vertical(id="top_hud"):
            yield FPSCounter(id="fps_counter")
            yield LocationHUD(id="location_hud")
            yield CompassHUD(id="compass_hud")

        with Horizontal(id="bottom_hud"):
            yield QuestHUD(id="quest_hud")
            yield StatsHUD(id="stats_hud")
            yield EntityModal(id="entity_modal")

        """Modal for showing notifications like "x item picked up"""""
        yield Notifications(id="notifications")
        yield Footer()

    def update_widgets(self):
        """Update the screen widgets."""
        game_view = self.query_one("#game_view", GameView)
        game_view.refresh()
        
        gs = self.app.game_state
        
        stats_hud = self.query_one("#stats_hud", StatsHUD)
        stats_hud.cash = gs.player_cash
        stats_hud.durability = int(gs.current_durability)
        stats_hud.max_durability = int(gs.max_durability)
        stats_hud.gas = gs.current_gas
        stats_hud.gas_capacity = int(gs.gas_capacity)
        stats_hud.speed = gs.car_speed
        stats_hud.level = gs.player_level
        stats_hud.xp = gs.current_xp
        stats_hud.xp_to_next_level = gs.xp_to_next_level
        stats_hud.pedal_position = gs.pedal_position
        
        # For now, just display the ammo for the first weapon
        first_weapon = next(iter(gs.mounted_weapons.values()), None)
        if first_weapon:
            stats_hud.ammo = gs.ammo_counts.get(first_weapon.ammo_type, 0)
            stats_hud.max_ammo = 999 # Placeholder for max ammo
        else:
            stats_hud.ammo = 0
            stats_hud.max_ammo = 0

        quest_hud = self.query_one("#quest_hud", QuestHUD)
        quest_hud.quest_name = gs.current_quest.name if gs.current_quest else "None"

        location = self.query_one("#location_hud", LocationHUD)
        location.x = int(gs.car_world_x)
        location.y = int(gs.car_world_y)
        grid_x = round(gs.car_world_x / CITY_SPACING)
        grid_y = round(gs.car_world_y / CITY_SPACING)
        location.city_name = get_city_name(grid_x, grid_y)

        compass = self.query_one("#compass_hud", CompassHUD)
        target_x, target_y, target_name = None, None, None
        
        if gs.waypoint:
            target_x, target_y = gs.waypoint
            target_name = "Waypoint"
        elif gs.current_quest:
            if gs.current_quest.ready_to_turn_in:
                # Point to quest giver
                target_x = gs.current_quest.city_id[0] * CITY_SPACING
                target_y = gs.current_quest.city_id[1] * CITY_SPACING
                target_name = "Turn In Quest"
            elif gs.current_quest.boss:
                # Point to boss
                boss = gs.current_quest.boss
                target_x, target_y = boss.x, boss.y
                target_name = boss.name
        
        if target_x is not None:
            angle_to_target = math.atan2(target_y - gs.car_world_y, target_x - gs.car_world_x)
            compass.target_angle = math.degrees(angle_to_target)
            compass.player_angle = gs.car_angle
            compass.target_name = target_name
        else:
            compass.target_angle = 0
            compass.player_angle = 0
            compass.target_name = ""

        # Update Entity Modal
        entity_modal = self.query_one("#entity_modal", EntityModal)
        closest_entity = self.app.find_closest_entity()
        if closest_entity:
            entity_modal.name = closest_entity["name"]
            entity_modal.hp = closest_entity["hp"]
            entity_modal.max_hp = closest_entity["max_hp"]
            entity_modal.art = closest_entity["art"]
            entity_modal.display = True
        else:
            entity_modal.display = False

        # Handle explosions
        for destroyed in gs.destroyed_this_frame:
            art = destroyed.art.get("N") if isinstance(destroyed.art, dict) else destroyed.art
            explosion = Explosion(art)
            self.mount(explosion)
            explosion.offset = (int(destroyed.x - gs.car_world_x + self.size.width / 2), 
                                int(destroyed.y - gs.car_world_y + self.size.height / 2))
        gs.destroyed_this_frame.clear()