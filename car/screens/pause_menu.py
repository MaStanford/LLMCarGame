from textual.screen import ModalScreen
from textual.widgets import Button
from ..logic.save_load import save_game

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
        elif event.button.id == "save_game":
            save_game(self.app.game_state)
            self.app.screen.query_one("#notifications").add_notification("Game Saved!")
            self.app.pop_screen()
        elif event.button.id == "main_menu":
            self.app.stop_game_loop()
            self.app.switch_screen("main_menu")
        elif event.button.id == "quit":
            self.app.exit()

