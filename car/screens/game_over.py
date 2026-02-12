from textual.screen import ModalScreen
from textual.widgets import Button, Static, Footer
from textual.containers import Vertical
from textual.binding import Binding
from .new_game import NewGameScreen
from .load_game import LoadGameScreen
from .main_menu import MainMenuScreen

class GameOverScreen(ModalScreen):
    """The game over screen."""

    BINDINGS = [
        Binding("up", "focus_previous", "Up", show=False),
        Binding("down", "focus_next", "Down", show=False),
        Binding("enter", "select_button", "Select", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focusable_widgets = []
        self.current_focus_index = 0

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

    def on_mount(self) -> None:
        """Set up the focusable widgets."""
        self.focusable_widgets = list(self.query("Button"))
        self.current_focus_index = 0
        self._update_focus()

    def _update_focus(self) -> None:
        """Update which widget has focus."""
        if self.focusable_widgets:
            self.focusable_widgets[self.current_focus_index].focus()

    def action_focus_previous(self) -> None:
        """Focus the previous widget."""
        if self.focusable_widgets:
            self.current_focus_index = (self.current_focus_index - 1 + len(self.focusable_widgets)) % len(self.focusable_widgets)
            self._update_focus()

    def action_focus_next(self) -> None:
        """Focus the next widget."""
        if self.focusable_widgets:
            self.current_focus_index = (self.current_focus_index + 1) % len(self.focusable_widgets)
            self._update_focus()

    def action_select_button(self) -> None:
        """Press the focused button."""
        if self.focusable_widgets:
            self.focusable_widgets[self.current_focus_index].press()

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
