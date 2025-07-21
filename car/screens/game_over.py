from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.containers import Vertical

class GameOverScreen(ModalScreen):
    """The game over screen."""

    def compose(self):
        """Compose the layout of the screen."""
        with Vertical(id="game-over-dialog"):
            yield Static("Game Over", id="game-over-title")
            yield Button("New Game", id="new_game", variant="primary")
            yield Button("Load Game", id="load_game", variant="default")
            yield Button("Quit", id="quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "new_game":
            self.app.stop_game_loop()
            self.app.switch_screen("new_game")
        elif event.button.id == "load_game":
            self.app.stop_game_loop()
            self.app.switch_screen("load_game")
        elif event.button.id == "quit":
            self.app.exit()