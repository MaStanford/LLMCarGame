from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical
from textual.binding import Binding
from ..logic.save_load import save_game

class SaveGameScreen(ModalScreen):
    """A modal screen for naming and saving the game."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("enter", "save_and_exit", "Save"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.save_name = ""

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Vertical(id="save_game_container"):
            yield Static("Enter Save Name:", id="save_prompt")
            yield Static(id="save_name_display", classes="panel")
            yield Button("Save", id="save_button", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.query_one("#save_name_display").update(self.save_name)

    def on_key(self, event) -> None:
        """Capture key presses to build the save name."""
        if event.is_printable:
            self.save_name += event.character
            self.query_one("#save_name_display").update(self.save_name)
        elif event.key == "backspace":
            self.save_name = self.save_name[:-1]
            self.query_one("#save_name_display").update(self.save_name)

    def action_save_and_exit(self) -> None:
        """Save the game and pop the screen."""
        from .world import WorldScreen # Moved import to break circular dependency
        if self.save_name:
            save_game(self.app.game_state, self.save_name)
            
            # Find the WorldScreen in the stack to post the notification
            world_screen = next((s for s in self.app.screen_stack if isinstance(s, WorldScreen)), None)
            if world_screen:
                world_screen.query_one("#notifications").add_notification(f"Game Saved as '{self.save_name}'!")

            self.app.pop_screen() # Pop the save screen
            self.app.pop_screen() # Pop the pause screen

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the save button."""
        if event.button.id == "save_button":
            self.action_save_and_exit()
