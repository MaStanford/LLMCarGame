from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Footer
from textual.binding import Binding

from .new_game import NewGameScreen
from .load_game import LoadGameScreen


class MainMenuScreen(Screen):
    """The main menu screen."""

    BINDINGS = [
        Binding("up", "focus_previous", "Up"),
        Binding("down", "focus_next", "Down"),
        Binding("enter", "select_button", "Select"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focusable_widgets = []
        self.current_focus_index = 0

    def compose(self) -> ComposeResult:
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Vertical(id="main-menu-buttons"):
            yield Button("New Game", id="new_game", variant="primary")
            yield Button("Load Game", id="load_game", variant="default")
            yield Button("Settings", id="settings", variant="default")
            yield Button("Quit", id="quit", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the initial state of the screen."""
        self.focusable_widgets = list(self.query(Button))
        self.focusable_widgets[self.current_focus_index].focus()

    def action_focus_previous(self) -> None:
        """Focus the previous widget."""
        self.current_focus_index = (self.current_focus_index - 1 + len(self.focusable_widgets)) % len(self.focusable_widgets)
        self.focusable_widgets[self.current_focus_index].focus()

    def action_focus_next(self) -> None:
        """Focus the next widget."""
        self.current_focus_index = (self.current_focus_index + 1) % len(self.focusable_widgets)
        self.focusable_widgets[self.current_focus_index].focus()

    def action_select_button(self) -> None:
        """Press the focused button."""
        self.focusable_widgets[self.current_focus_index].press()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "new_game":
            self.app.push_screen(NewGameScreen())
        elif event.button.id == "load_game":
            self.app.push_screen(LoadGameScreen())
        elif event.button.id == "settings":
            # We'll add the settings screen later
            pass
        elif event.button.id == "quit":
            self.app.exit()
