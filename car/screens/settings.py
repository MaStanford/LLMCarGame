from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Static
from textual.binding import Binding

from ..config import load_settings, save_settings

class SettingsScreen(Screen):
    """A screen for changing game settings."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.settings = load_settings()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="settings-container"):
                yield Static("[bold]Settings[/bold]", id="title")
                
                yield Static("World Generation Mode", classes="setting-label")
                yield Button(self.get_mode_label(), id="toggle_mode")

                yield Button("Back", id="back", variant="primary")
        yield Footer(show_command_palette=True)

    def get_mode_label(self) -> str:
        """Returns the display label for the current generation mode."""
        mode = self.settings.get("generation_mode", "local")
        return f"Mode: {mode.replace('_', ' ').title()}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "toggle_mode":
            current_mode = self.settings.get("generation_mode", "local")
            new_mode = "gemini_cli" if current_mode == "local" else "local"
            self.settings["generation_mode"] = new_mode
            save_settings(self.settings)
            event.button.label = self.get_mode_label()
            self.app.generation_mode = new_mode # Update the app instance
        elif event.button.id == "back":
            self.app.pop_screen()
