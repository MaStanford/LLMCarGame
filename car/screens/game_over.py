from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.containers import Vertical

class GameOverScreen(ModalScreen):
    """A modal screen for the game over state."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="game-over-dialog"):
            yield Static("GAME OVER!", id="game-over-title")
            yield Static(self.message, id="game-over-message")
            yield Button("Play Again", variant="primary", id="play-again")
            yield Button("Exit", variant="error", id="exit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play-again":
            # This is a bit tricky. We need to tell the app to restart the game.
            # A custom event or a callback would be ideal here.
            # For now, we'll just pop this screen and the main menu will handle it.
            self.app.pop_screen() # Pop self
            self.app.pop_screen() # Pop DefaultScreen
            from .main_menu import MainMenuScreen
            self.app.push_screen(MainMenuScreen())
        elif event.button.id == "exit":
            self.app.exit()
