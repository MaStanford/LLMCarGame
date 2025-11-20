from textual.screen import ModalScreen
from textual.widgets import Button, Static, Footer
from textual.containers import Vertical
from .new_game import NewGameScreen
from .load_game import LoadGameScreen
from .main_menu import MainMenuScreen

class GameOverScreen(ModalScreen):
    """The game over screen."""

    def compose(self):
        """Compose the layout of the screen."""
        with Vertical(id="game-over-dialog"):
            yield Static("Game Over", id="game-over-title")
            yield Static("Your journey has come to an end.", id="game-over-text")
            yield Button("New Game", id="new_game", variant="primary")
            yield Button("Load Game", id="load_game", variant="default")
            yield Button("Main Menu", id="main_menu", variant="default")
            yield Button("Quit", id="quit", variant="error")
        yield Footer(show_command_palette=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "new_game":
            self.app.stop_game_loop()
            self.app.switch_screen(NewGameScreen())
        elif event.button.id == "load_game":
            self.app.stop_game_loop()
            self.app.switch_screen(LoadGameScreen())
        elif event.button.id == "main_menu":
            self.app.stop_game_loop()
            self.app.switch_screen(MainMenuScreen())
        elif event.button.id == "quit":
            self.app.exit()
