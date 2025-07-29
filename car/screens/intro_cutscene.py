from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Header, Footer, Button
from textual.containers import Center, Vertical
from textual.binding import Binding

class IntroCutsceneScreen(Screen):
    """A screen to display the introductory story text."""

    BINDINGS = [
        Binding("enter", "end_cutscene", "Continue"),
    ]

    def __init__(self, intro_text: str) -> None:
        super().__init__()
        self.intro_text = intro_text

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="intro-cutscene-container"):
                yield Static(self.intro_text, id="intro-text")
                yield Button("Continue", id="continue", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle the continue button press."""
        if event.button.id == "continue":
            self.action_end_cutscene()

    def action_end_cutscene(self) -> None:
        """Switches to the main game world screen."""
        from .world import WorldScreen
        self.app.switch_screen(WorldScreen())
        self.app.game_loop = self.app.set_interval(1 / 30, self.app.update_game)
