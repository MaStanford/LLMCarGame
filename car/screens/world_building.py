import logging
import time
import random
from functools import partial
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer, ProgressBar
from textual.worker import Worker, WorkerState

from ..game_state import GameState
from ..world import World
from ..workers.world_generator import generate_initial_world_worker, StageUpdate
from ..data.difficulty import DIFFICULTY_MODIFIERS

class WorldBuildingScreen(Screen):
    """A screen that shows the progress of the world being built, with flair."""

    BINDINGS = []

    def __init__(self, new_game_settings: dict) -> None:
        super().__init__()
        self.new_game_settings = new_game_settings
        self.world_data = None
        self.status_messages = [
            "Calibrating wasteland frequencies...",
            "Reticulating splines...",
            "Generating continental plates...",
            "Simulating tectonic shifts...",
            "Spooling up the reality matrix...",
            "Calculating factional friction...",
            "Plotting ley lines...",
            "Seeding initial conflicts...",
            "Negotiating with rogue AIs...",
            "Polishing chrome skulls...",
            "Untangling quantum supply lines...",
            "Drawing new world map... (This may take a few minutes)",
            "Finalizing timeline...",
        ]
        self.current_message_index = 0
        self.animation_chars = "░▒▓█▄▀▌▐─█│┌┐└┘ℍ├┤┬┴┼═‗║₪╔╗╚╝╠╣╦╩╬▤▥▦▧▨▩"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical(id="world-building-container"):
            yield Static(id="animation_display", classes="world-building-animation")
            yield Static("", id="title") # Title will be set dynamically
            yield ProgressBar(id="progress", total=None, show_percentage=False, show_eta=False)
            yield Static(self.status_messages[0], id="status_message")
        yield Footer()

    def on_mount(self) -> None:
        """Start the world generation process."""
        # Set the dynamic title
        theme_name = self.new_game_settings.get("theme", {}).get("name", "the Wasteland")
        self.query_one("#title", Static).update(f"[bold]Bringing '{theme_name}' to Life...[/bold]\nThis may take a few minutes.")

        self.set_interval(2.5, self.update_status_message)
        self.set_interval(0.05, self.update_animation)

        # Start the world generation worker
        self.run_worker(
            partial(generate_initial_world_worker, self.app, self.new_game_settings),
            exclusive=True,
            thread=True,
            name="WorldGenerator"
        )

    def update_status_message(self) -> None:
        """Cycle through the status messages."""
        self.current_message_index = (self.current_message_index + 1) % len(self.status_messages)
        self.query_one("#status_message", Static).update(self.status_messages[self.current_message_index])

    def update_animation(self) -> None:
        """Update the decorative animation with random characters."""
        animation_widget = self.query_one("#animation_display")
        width = 50
        height = 8
        lines = []
        for _ in range(height):
            lines.append("".join(random.choice(self.animation_chars) for _ in range(width)))
        animation_widget.update("\n".join(lines))

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        if event.worker.name == "WorldGenerator":
            if event.worker.state == WorkerState.SUCCESS:
                self.world_data = event.worker.result
                if self.world_data:
                    logging.info("World generation successful. Starting game.")
                    self.start_game()
                else:
                    logging.error("World generation failed: No data returned.")
                    self.query_one("#status_message").update("[bold red]Error: LLM returned no data.[/bold red]")
                    self.query_one(ProgressBar).display = False
                    self.query_one("#world-building-container").mount(Button("Retry", id="retry", variant="error"))
            elif event.worker.state == WorkerState.ERROR:
                error_message = str(event.worker.error)
                logging.error(f"World generator worker failed: {error_message}")
                self.query_one("#status_message").update(f"[bold red]Error: {error_message}[/bold red]")
                self.query_one(ProgressBar).display = False
                self.query_one("#world-building-container").mount(Button("Retry", id="retry", variant="error"))

    def on_stage_update(self, event: StageUpdate) -> None:
        """Handle stage update messages from the worker."""
        # The original on_worker_message was changed to on_stage_update and now expects a StageUpdate event.
        # The content of the method remains the same as it correctly handles the 'stage' message type.
        if event.message_type == "stage":
            self.query_one("#title", Static).update(f"[bold]{event.data}[/bold]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle retry button press."""
        if event.button.id == "retry":
            event.button.remove()
            self.query_one(ProgressBar).display = True
            self.query_one("#status_message").update(self.status_messages[0])
            self.on_mount() # Re-run the generation

    def start_game(self) -> None:
        """Finalizes game state and switches to the intro cutscene."""
        from .intro_cutscene import IntroCutsceneScreen
        from ..logic.save_load import load_triggers
        import os
        import shutil
        import pprint
        import json

        # Save the new faction data
        if os.path.exists("temp"):
            shutil.rmtree("temp")
        os.makedirs("temp")
        with open("temp/factions.py", "w") as f:
            f.write("FACTION_DATA = ")
            pprint.pprint(self.world_data["factions"], stream=f, indent=4)
            
        # Save the new world details
        with open("temp/world_details.json", "w") as f:
            json.dump(self.world_data["world_details"], f, indent=4)

        # CRITICAL: Reload the data modules to load the new factions
        self.app.reload_dynamic_data()

        difficulty = self.new_game_settings["difficulty"]
        
        # Create the game state
        game_state = GameState(
            selected_car_index=self.new_game_settings["selected_car_index"],
            difficulty=difficulty,
            difficulty_mods=self.new_game_settings["difficulty_mods"],
            car_color_names=[self.new_game_settings["car_color_name"]],
            theme=self.new_game_settings["theme"],
            factions=self.world_data["factions"],
        )
        game_state.world_details = self.world_data["world_details"]
        
        # Save the generated story intro to the game state
        game_state.story_intro = self.world_data["story_intro"]
        
        # Pre-populate the quest cache
        neutral_city_id = self.world_data["neutral_city_id"]
        game_state.quest_cache[neutral_city_id] = self.world_data["quests"]
        
        # Load triggers
        load_triggers(game_state)
        
        # Set player position
        game_state.car_world_x = 10.0
        game_state.car_world_y = 10.0
        game_state.player_car.x = game_state.car_world_x
        game_state.player_car.y = game_state.car_world_y
        
        self.app.game_state = game_state
        self.app.world = World(seed=int(time.time()))
        
        # Switch to the intro cutscene
        self.app.switch_screen(IntroCutsceneScreen(self.world_data["story_intro"]))
