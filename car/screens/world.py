import math
import logging

from textual.screen import Screen
from textual.widgets import Static
from textual.containers import Horizontal, Vertical, Container

from ..data.game_constants import CITY_SPACING
from ..widgets.entity_modal import EntityModal
from ..widgets.explosion import Explosion
from ..widgets.hud_stats import StatsHUD
from ..widgets.hud_location import LocationHUD
from ..widgets.hud_compass import CompassHUD
from ..widgets.hud_quest import QuestHUD
from ..widgets.game_view import GameView
from ..widgets.notifications import Notifications
from ..widgets.fps_counter import FPSCounter
from ..world.generation import get_city_name
from ..logic.spawning import spawn_initial_entities

from textual.events import Key

class WorldScreen(Screen):
    """The default screen for the game."""

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        # Set sensible spawn and despawn radii based on screen size
        corner_distance = math.sqrt((self.size.width / 2)**2 + (self.size.height / 2)**2)
        self.app.game_state.spawn_radius = corner_distance + 5 # Spawn just outside the corner
        self.app.game_state.despawn_radius = self.app.game_state.spawn_radius * 1.5
        
        self.query_one("#game_view").focus()

    def compose(self):
        """Compose the layout of the screen."""
        yield GameView(id="game_view", game_state=self.app.game_state, world=self.app.world)
        
        with Vertical(id="top_hud"):
            # yield FPSCounter(id="fps_counter")
            yield LocationHUD(id="location_hud")
            yield CompassHUD(id="compass_hud")

        with Horizontal(id="bottom_hud"):
            yield QuestHUD(id="quest_hud")
            yield StatsHUD(id="stats_hud")
            yield EntityModal(id="entity_modal")

        """Modal for showing notifications like "x item picked up"""""
        yield Notifications(id="notifications")

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

        quest_hud = self.query_one("#quest_hud", QuestHUD)
        quest_hud.quest_name = gs.current_quest.name if gs.current_quest else "None"

        location = self.query_one("#location_hud", LocationHUD)
        location.x = int(gs.car_world_x)
        location.y = int(gs.car_world_y)
        grid_x = round(gs.car_world_x / CITY_SPACING)
        grid_y = round(gs.car_world_y / CITY_SPACING)
        location.city_name = get_city_name(grid_x, grid_y)

        compass = self.query_one("#compass_hud", CompassHUD)
        if gs.current_quest and gs.current_quest.boss:
            boss = gs.current_quest.boss
            angle_to_boss = math.atan2(boss.y - gs.car_world_y, boss.x - gs.car_world_x)
            compass.target_angle = math.degrees(angle_to_boss)
            compass.player_angle = gs.car_angle
        else:
            compass.target_angle = 0
            compass.player_angle = 0

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




