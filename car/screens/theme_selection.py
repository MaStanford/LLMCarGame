import logging
from functools import partial
from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer, LoadingIndicator
from textual.worker import Worker, WorkerState

from .world_building import WorldBuildingScreen
from ..logic.llm_theme_generator import generate_themes_from_llm

class ThemeSelectionScreen(Screen):
    """A screen for the player to choose a narrative theme."""

    def __init__(self, new_game_settings: dict) -> None:
        super().__init__()
        self.new_game_settings = new_game_settings

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Center():
            with Vertical(id="theme-selection-container"):
                yield Static("[bold]Select a Theme[/bold]", id="title")
                yield Static("The world is waiting to be born. Choose its flavor.\nThis may take a minute...", id="subtitle")
                yield LoadingIndicator()
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

        self.query_one(LoadingIndicator).display = True
        self.query_one("#reincarnate", Button).disabled = True
        self.query_one("#subtitle").update("The world is waiting to be born. Choose its flavor.\nThis may take a minute...")


        self.run_worker(
            partial(generate_themes_from_llm, self.app),
            exclusive=True,
            thread=True,
            name="ThemeGenerator"
        )

    def on_mount(self) -> None:
        """Start the initial theme generation process."""
        self._generate_themes()

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the theme generator worker state changes."""
        if event.worker.name == "ThemeGenerator":
            loading_indicator = self.query_one(LoadingIndicator)
            buttons_container = self.query_one("#theme-buttons-container")
            reincarnate_button = self.query_one("#reincarnate", Button)

            if event.worker.state == WorkerState.SUCCESS:
                loading_indicator.display = False
                reincarnate_button.disabled = False
                themes = event.worker.result
                if themes:
                    for i, theme in enumerate(themes):
                        button = Button(f"{theme['name']}\n\n[italic]{theme['description']}[/italic]", id=f"theme_{i}", variant="primary")
                        button.theme_data = theme
                        buttons_container.mount(button)
                else:
                    self.query_one("#subtitle").update("[bold red]Error: Could not generate themes.[/bold red]")
            elif event.worker.state == WorkerState.ERROR:
                loading_indicator.display = False
                reincarnate_button.disabled = False
                self.query_one("#subtitle").update("[bold red]Error: Theme worker failed.[/bold red]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle theme selection or reincarnation."""
        if event.button.id.startswith("theme_"):
            selected_theme = event.button.theme_data
            self.new_game_settings["theme"] = selected_theme
            self.app.switch_screen(WorldBuildingScreen(self.new_game_settings))
        elif event.button.id == "reincarnate":
            self._generate_themes()
