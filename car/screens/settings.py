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

                yield Static("Dev Mode", classes="setting-label")
                yield Button(self.get_dev_mode_label(), id="toggle_dev_mode")

                yield Button("Back", id="back", variant="primary")
        yield Footer()

    def get_mode_label(self) -> str:
        """Returns the display label for the current generation mode."""
        mode = self.settings.get("generation_mode", "local")
        return f"Mode: {mode.replace('_', ' ').title()}"

    def get_dev_mode_label(self) -> str:
        """Returns the display label for the dev mode."""
        dev_mode = self.settings.get("dev_mode", False)
        return f"Dev Mode: {'On' if dev_mode else 'Off'}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "toggle_mode":
            current_mode = self.settings.get("generation_mode", "local")
            new_mode = "gemini_cli" if current_mode == "local" else "local"
            
            # Check auth if switching TO Gemini CLI
            if new_mode == "gemini_cli":
                from ..logic.gemini_cli import check_gemini_auth
                if not check_gemini_auth():
                    self.notify("Warning: Gemini CLI not authenticated! Run 'gemini auth' in terminal.", severity="warning", timeout=5.0)

            self.settings["generation_mode"] = new_mode
            save_settings(self.settings)
            event.button.label = self.get_mode_label()
            self.app.generation_mode = new_mode # Update the app instance
        elif event.button.id == "toggle_dev_mode":
            current_dev_mode = self.settings.get("dev_mode", False)
            new_dev_mode = not current_dev_mode
            self.settings["dev_mode"] = new_dev_mode
            save_settings(self.settings)
            event.button.label = self.get_dev_mode_label()
            self.app.dev_mode = new_dev_mode # Update the app instance
        elif event.button.id == "back":
            self.app.pop_screen()
