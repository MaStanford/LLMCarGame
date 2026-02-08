from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Static
from textual.binding import Binding

from ..config import load_settings, save_settings
from ..logic.gemini_cli import CLI_PRESETS, check_cli_auth

class SettingsScreen(Screen):
    """A screen for changing game settings."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    CLI_PRESET_CYCLE = ["gemini", "claude", "custom"]

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

                yield Static("Local Model Size", classes="setting-label")
                yield Button(self.get_model_size_label(), id="toggle_model_size")

                yield Static("CLI LLM Tool (for CLI mode)", classes="setting-label")
                yield Button(self.get_cli_preset_label(), id="toggle_cli_preset")

                yield Static("Dev Mode", classes="setting-label")
                yield Button(self.get_dev_mode_label(), id="toggle_dev_mode")

                yield Button("Back", id="back", variant="primary")
        yield Footer()

    def get_mode_label(self) -> str:
        """Returns the display label for the current generation mode."""
        mode = self.settings.get("generation_mode", "local")
        if mode == "local":
            return "Mode: Local LLM"
        return "Mode: CLI LLM"

    def get_model_size_label(self) -> str:
        """Returns the display label for the model size."""
        size = self.settings.get("model_size", "small")
        names = {"small": "Small (Qwen3-4B)", "large": "Large (Qwen3-8B)"}
        return f"Model: {names.get(size, size)}"

    def get_cli_preset_label(self) -> str:
        """Returns the display label for the CLI LLM preset."""
        preset = self.settings.get("cli_preset", "gemini")
        if preset == "custom":
            cmd = self.settings.get("custom_cli_command", "") or "not set"
            return f"CLI Tool: Custom ({cmd})"
        desc = CLI_PRESETS.get(preset, {}).get("description", preset)
        return f"CLI Tool: {desc}"

    def get_dev_mode_label(self) -> str:
        """Returns the display label for the dev mode."""
        dev_mode = self.settings.get("dev_mode", False)
        return f"Dev Mode: {'On' if dev_mode else 'Off'}"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "toggle_mode":
            current_mode = self.settings.get("generation_mode", "local")
            new_mode = "gemini_cli" if current_mode == "local" else "local"

            # Check auth if switching TO CLI mode
            if new_mode == "gemini_cli":
                preset = self.settings.get("cli_preset", "gemini")
                if not check_cli_auth(preset):
                    tool_name = CLI_PRESETS.get(preset, {}).get("description", preset)
                    self.notify(f"Warning: {tool_name} not found or not authenticated!", severity="warning", timeout=5.0)

            self.settings["generation_mode"] = new_mode
            save_settings(self.settings)
            event.button.label = self.get_mode_label()
            self.app.generation_mode = new_mode
        elif event.button.id == "toggle_model_size":
            current = self.settings.get("model_size", "small")
            new_size = "large" if current == "small" else "small"
            self.settings["model_size"] = new_size
            save_settings(self.settings)
            event.button.label = self.get_model_size_label()
            self.app.model_size = new_size
            # Force model reload on next main menu visit
            self.app.llm_pipeline = None
            self.notify("Model size changed. Will reload on return to main menu.", severity="information", timeout=3.0)
        elif event.button.id == "toggle_cli_preset":
            current = self.settings.get("cli_preset", "gemini")
            try:
                idx = self.CLI_PRESET_CYCLE.index(current)
            except ValueError:
                idx = -1
            new_preset = self.CLI_PRESET_CYCLE[(idx + 1) % len(self.CLI_PRESET_CYCLE)]

            self.settings["cli_preset"] = new_preset
            save_settings(self.settings)
            event.button.label = self.get_cli_preset_label()
            self.app.cli_preset = new_preset

            # Validate the new preset
            if new_preset == "custom":
                cmd = self.settings.get("custom_cli_command", "")
                if not cmd:
                    self.notify("Custom CLI: Set 'custom_cli_command' in settings.json", severity="warning", timeout=5.0)
            elif not check_cli_auth(new_preset):
                tool_name = CLI_PRESETS.get(new_preset, {}).get("description", new_preset)
                self.notify(f"{tool_name} not found or not authenticated.", severity="warning", timeout=5.0)
            else:
                tool_name = CLI_PRESETS.get(new_preset, {}).get("description", new_preset)
                self.notify(f"CLI tool set to {tool_name}.", severity="information", timeout=3.0)
        elif event.button.id == "toggle_dev_mode":
            current_dev_mode = self.settings.get("dev_mode", False)
            new_dev_mode = not current_dev_mode
            self.settings["dev_mode"] = new_dev_mode
            save_settings(self.settings)
            event.button.label = self.get_dev_mode_label()
            self.app.dev_mode = new_dev_mode
        elif event.button.id == "back":
            self.app.pop_screen()
