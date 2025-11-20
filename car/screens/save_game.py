from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button, Input, Footer
from textual.containers import Vertical
from textual.binding import Binding
from ..logic.save_load import save_game

class SaveGameScreen(ModalScreen):
    """A modal screen for naming and saving the game."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        with Vertical(id="save_game_container"):
            yield Static("Enter Save Name:", id="save_prompt")
            yield Input(placeholder="Wasteland Adventure", id="save_name_input")
            yield Button("Save", id="save_button", variant="primary")
        yield Footer(show_command_palette=True)

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.query_one(Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the save button."""
        if event.button.id == "save_button":
            save_name = self.query_one(Input).value
            if save_name:
                # --- Update GameState with current position before saving ---
                gs = self.app.game_state
                gs.car_world_x = self.app.game_state.car_world_x
                gs.car_world_y = self.app.game_state.car_world_y
                
                save_game(gs, save_name)
                
                # Find the WorldScreen to post the notification
                from .world import WorldScreen
                world_screen = next((s for s in self.app.screen_stack if isinstance(s, WorldScreen)), None)
                if world_screen:
                    world_screen.query_one("#notifications").add_notification(f"Game Saved as '{save_name}'!")

                self.app.pop_screen() # Pop the save screen
                self.app.pop_screen() # Pop the pause screen
            else:
                # Optionally, provide feedback that a name is required
                pass