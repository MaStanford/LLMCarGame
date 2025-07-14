from textual.screen import Screen
from ..widgets.game_view import GameView
from ..widgets.hud import HUD
from ..widgets.controls import Controls
from ..widgets.entity_modal import EntityModal
from ..widgets.location import Location
from ..widgets.notifications import Notifications
from textual.events import Key

class DefaultScreen(Screen):
    """The default screen for the game."""

    def compose(self):
        """Compose the layout of the screen."""
        yield GameView(id="game_view", game_state=self.app.game_state, world=self.app.world)
        yield HUD(id="hud")
        yield Controls(id="controls")
        yield Location(id="location")
        yield EntityModal(id="entity_modal")
        yield Notifications(id="notifications")

    def frame_update(self, gs):
        """Update the screen widgets."""
        self.query_one("#game_view", GameView).refresh()
        
        hud = self.query_one("#hud", HUD)
        hud.cash = gs.player_cash
        hud.durability = int(gs.current_durability)
        hud.max_durability = int(gs.max_durability)
        hud.gas = gs.current_gas
        hud.gas_capacity = int(gs.gas_capacity)
        hud.speed = gs.car_speed

        location = self.query_one("#location", Location)
        location.x = int(gs.car_world_x)
        location.y = int(gs.car_world_y)

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

    def on_key(self, event: Key) -> None:
        """Handle key presses for game actions."""
        gs = self.app.game_state
        if event.key == "w":
            gs.actions["accelerate"] = True
        elif event.key == "s":
            gs.actions["brake"] = True
        elif event.key == "a":
            gs.actions["turn_left"] = True
        elif event.key == "d":
            gs.actions["turn_right"] = True
        elif event.key == "space":
            gs.actions["fire"] = True
        else:
            gs.actions["accelerate"] = False
            gs.actions["brake"] = False
            gs.actions["turn_left"] = False
            gs.actions["turn_right"] = False
            gs.actions["fire"] = False




