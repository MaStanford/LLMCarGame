import logging
from functools import partial
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, ProgressBar, Static
from textual.binding import Binding
from textual.worker import Worker, WorkerState

from .new_game import NewGameScreen
from .load_game import LoadGameScreen
from .settings import SettingsScreen
from ..workers.model_loader import load_pipeline

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
        yield Header(show_clock=True, name="The Genesis Module")
        with Vertical(id="main-menu-container"):
            with Vertical(id="main-menu-buttons"):
                yield Button("New Game", id="new_game", variant="primary", disabled=True)
                yield Button("Load Game", id="load_game", variant="default", disabled=True)
                yield Button("Settings", id="settings", variant="default")
                yield Button("Quit", id="quit", variant="error")
            with Vertical(id="model-loader-container"):
                yield Static("Loading LLM Model...", id="model_status")
                yield ProgressBar(id="model_progress", show_eta=False)
        yield Footer()

    def on_mount(self) -> None:
        """Set up the initial state of the screen."""
        logging.info("MainMenuScreen mounted.")
        self.focusable_widgets = list(self.query("Button"))
        self._update_ui_for_mode()

    def on_screen_resume(self) -> None:
        """Called when returning to this screen from another."""
        self._update_ui_for_mode()

    def _update_ui_for_mode(self):
        """Checks the generation mode and updates the UI accordingly."""
        self.focusable_widgets[self.current_focus_index].focus()
        
        if self.app.generation_mode == "gemini_cli":
            logging.info("Gemini CLI mode is active. Skipping local model load.")
            self.query_one("#model_status", Static).update("Ready (Gemini CLI)")
            self.query_one(ProgressBar).display = False
            self.query_one("#new_game").disabled = False
            self.query_one("#load_game").disabled = False
        else:
            # Local mode, check if model is already loaded or loading
            if self.app.llm_pipeline is None:
                model_size = self.app.model_size
                logging.info(f"Local mode active. Starting model loader worker (size={model_size})...")
                self.query_one("#model_status", Static).update(f"Loading LLM Model ({model_size})...")
                self.query_one(ProgressBar).display = True
                self.query_one("#new_game").disabled = True
                self.query_one("#load_game").disabled = True
                self.run_worker(
                    partial(load_pipeline, model_size=model_size),
                    exclusive=True, thread=True, name="load_pipeline"
                )
            else:
                logging.info("Local mode active. Model already loaded.")
                self.query_one("#model_status", Static).update("LLM model loaded.")
                self.query_one(ProgressBar).display = False
                self.query_one("#new_game").disabled = False
                self.query_one("#load_game").disabled = False

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        logging.info(f"Worker {event.worker.name} changed state to {event.worker.state}")
        if event.worker.name == "load_pipeline":
            if event.worker.state == WorkerState.SUCCESS:
                pipeline = event.worker.result
                if pipeline:
                    logging.info("Model loaded successfully! Hiding loader and enabling buttons.")
                    self.app.llm_pipeline = pipeline
                    self._update_ui_for_mode()
                else:
                    logging.error("Model loading failed in worker.")
                    self.query_one("#model_status", Static).update("Error: Model failed to load.")
                    self.query_one(ProgressBar).display = False
            elif event.worker.state == WorkerState.ERROR:
                logging.error(f"Worker failed with state {event.worker.state}")
                self.query_one("#model_status", Static).update("Error: Worker failed.")
                self.query_one(ProgressBar).display = False


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
            self.app.push_screen(SettingsScreen())
        elif event.button.id == "quit":
            self.app.exit()
