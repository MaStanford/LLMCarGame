from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button, Input, Footer
from textual.containers import Vertical
from textual.binding import Binding
from ..logic.save_load import save_game

class SaveGameScreen(ModalScreen):
    """A modal screen for naming and saving the game."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
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
        input_widget = self.query_one(Input)
        # Prepopulate with the current save name if one exists
        current_name = getattr(self.app, 'current_save_name', None)
        if current_name:
            input_widget.value = current_name
        input_widget.focus()

    def _do_save(self) -> None:
        """Perform the save operation."""
        save_name = self.query_one(Input).value.strip()
        if not save_name:
            return

        gs = self.app.game_state
        save_game(gs, save_name)
        self.app.current_save_name = save_name

        # Find the WorldScreen to post the notification
        from .world import WorldScreen
        world_screen = next((s for s in self.app.screen_stack if isinstance(s, WorldScreen)), None)
        if world_screen:
            world_screen.query_one("#notifications").add_notification(f"Game Saved as '{save_name}'!")

        self.app.pop_screen()  # Pop the save screen
        self.app.pop_screen()  # Pop the pause screen

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key in the input field."""
        self._do_save()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the save button."""
        if event.button.id == "save_button":
            self._do_save()