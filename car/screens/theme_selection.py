import logging
import random
from functools import partial
from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer, ProgressBar
from textual.binding import Binding
from textual.worker import Worker, WorkerState

from .world_building import WorldBuildingScreen
from ..logic.llm_theme_generator import generate_themes_from_llm

class ThemeSelectionScreen(Screen):
    """A screen for the player to choose a narrative theme."""

    BINDINGS = [
        Binding("up", "focus_previous", "Up"),
        Binding("down", "focus_next", "Down"),
        Binding("enter", "select_button", "Select"),
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self, new_game_settings: dict) -> None:
        super().__init__()
        self.new_game_settings = new_game_settings
        self.focusable_widgets = []
        self.current_focus_index = 0
        # Animation state — symbols that feel "thematic" and mystical
        self.animation_chars = "◆◇○●□■△▲▽▼☆★♦♣♠♥◈◉◎⬡⬢⟐⟡✦✧⊕⊗⊙⊛"
        self.animation_phase = 0
        # Three column centers where "themes" will crystallize (within a 60-wide field)
        self.col_centers = [14, 30, 46]
        self.col_radius = 3

    def _get_cli_test_hint(self) -> str:
        """Returns a helpful hint for testing the CLI LLM tool."""
        if self.app.generation_mode == "gemini_cli":
            preset = getattr(self.app, 'cli_preset', 'gemini')
            if preset == "claude":
                return '\nTest your Claude CLI with: [bold]claude -p "say hi"[/bold]'
            elif preset == "gemini":
                return '\nTest your Gemini CLI with: [bold]gemini "say hi"[/bold]'
            else:
                return "\nCheck that your custom CLI tool is installed and working."
        return ""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="theme-selection-container"):
                yield Static("[bold]Select a Theme[/bold]", id="title")
                yield Static("The world is waiting to be born. Choose its flavor.\nThis may take a minute...", id="subtitle")
                yield ProgressBar(id="theme_progress", total=None, show_percentage=False, show_eta=False)
                yield Static(id="animation_display", classes="theme-animation")
                with Vertical(id="theme-buttons-container"):
                    # Buttons will be added here dynamically
                    pass
                yield Button("Reincarnate", id="reincarnate", variant="default", disabled=True)
        yield Footer()

    def _generate_themes(self) -> None:
        """Clears old themes and starts the generation worker."""
        buttons_container = self.query_one("#theme-buttons-container")
        # Clear any existing theme buttons
        for button in buttons_container.query(Button):
            button.remove()

        self.query_one("#animation_display").display = True
        self.query_one("#theme_progress", ProgressBar).display = True
        self.query_one("#reincarnate", Button).disabled = True
        self.query_one("#subtitle").update("The world is waiting to be born. Choose its flavor.\nThis may take a minute...")
        self.animation_phase = 0

        self.run_worker(
            partial(generate_themes_from_llm, self.app),
            exclusive=True,
            thread=True,
            name="ThemeGenerator"
        )

    def on_mount(self) -> None:
        """Start the initial theme generation process."""
        self.set_interval(0.06, self.update_animation)
        self._generate_themes()

    def update_animation(self) -> None:
        """Animate symbols converging from chaos into three columns.

        The full cycle:
          Phase 0-50:  Whittling — characters outside the 3 column bands
                       gradually fade to empty space.
          Phase 51-70: Hold — only the 3 crystallized columns remain,
                       still churning with random symbols.
          Phase 71-85: Refill — the field floods back to full density.
        Then it loops.
        """
        widget = self.query_one("#animation_display")
        if not widget.display:
            return

        width = 60
        height = 6

        self.animation_phase += 1
        cycle_len = 85
        pos = self.animation_phase % cycle_len

        if pos < 50:
            # Whittling: probability of hiding non-column cells increases
            fade = pos / 50.0
        elif pos < 70:
            # Hold: only 3 columns visible
            fade = 1.0
        else:
            # Refill: everything comes back
            fade = 1.0 - (pos - 70) / 15.0

        lines = []
        for _ in range(height):
            line = ""
            for x in range(width):
                in_column = any(abs(x - c) <= self.col_radius for c in self.col_centers)

                if in_column:
                    # Column cells always show — these are the 3 surviving themes
                    line += random.choice(self.animation_chars)
                else:
                    # Background cells fade away during the whittling phase
                    if random.random() > fade:
                        line += random.choice(self.animation_chars)
                    else:
                        line += " "
            lines.append(line)

        widget.update("\n".join(lines))

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the theme generator worker state changes."""
        if event.worker.name == "ThemeGenerator":
            progress_bar = self.query_one("#theme_progress", ProgressBar)
            buttons_container = self.query_one("#theme-buttons-container")
            reincarnate_button = self.query_one("#reincarnate", Button)

            if event.worker.state == WorkerState.SUCCESS:
                progress_bar.display = False
                self.query_one("#animation_display").display = False
                reincarnate_button.disabled = False
                result = event.worker.result
                if result:
                    themes, is_fallback = result
                    if is_fallback:
                        cli_hint = self._get_cli_test_hint()
                        self.query_one("#subtitle").update(
                            "[bold yellow]LLM unavailable — showing default themes.[/bold yellow]\n"
                            f"Check Settings > Generation Mode and ensure your LLM is configured.{cli_hint}\n"
                            "Press 'Reincarnate' to retry."
                        )
                    else:
                        self.query_one("#subtitle").update("Choose your world's theme.")
                    for i, theme in enumerate(themes):
                        button = Button(f"{theme['name']}\n\n[italic]{theme['description']}[/italic]", id=f"theme_{i}", variant="primary")
                        button.theme_data = theme
                        buttons_container.mount(button)
                    self._refresh_focusable_widgets()
                else:
                    cli_hint = self._get_cli_test_hint()
                    self.query_one("#subtitle").update(
                        "[bold red]Error: Could not generate themes.[/bold red]"
                        f"{cli_hint}"
                    )
                    self._refresh_focusable_widgets()
            elif event.worker.state == WorkerState.ERROR:
                progress_bar.display = False
                self.query_one("#animation_display").display = False
                reincarnate_button.disabled = False
                cli_hint = self._get_cli_test_hint()
                self.query_one("#subtitle").update(
                    "[bold red]Error: Theme worker failed.[/bold red]"
                    f"{cli_hint}"
                )
                self._refresh_focusable_widgets()

    def _refresh_focusable_widgets(self) -> None:
        """Rebuild the focusable widget list after buttons change."""
        self.focusable_widgets = [b for b in self.query("Button") if not b.disabled]
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
        """Handle theme selection or reincarnation."""
        if event.button.id.startswith("theme_"):
            selected_theme = event.button.theme_data
            self.new_game_settings["theme"] = selected_theme
            self.app.switch_screen(WorldBuildingScreen(self.new_game_settings))
        elif event.button.id == "reincarnate":
            self._generate_themes()
