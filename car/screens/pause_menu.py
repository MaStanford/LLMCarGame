from textual.screen import ModalScreen
from textual.widgets import Button

class PauseScreen(ModalScreen):
    """The pause menu screen."""

    def compose(self):
        """Compose the layout of the screen."""
        yield Button("Resume", id="resume", variant="primary")
        yield Button("Save Game", id="save_game", variant="default")
        yield Button("Main Menu", id="main_menu", variant="default")
        yield Button("Quit", id="quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "resume":
            self.app.pop_screen()
        elif event.button.id == "quit":
            self.app.exit()
        # We will add logic for save_game and main_menu later
