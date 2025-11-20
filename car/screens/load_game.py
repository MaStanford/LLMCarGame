import logging
import time
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable
from textual.binding import Binding
from textual.events import Key
from ..logic.save_load import get_save_slots, load_game
from ..world import World
import importlib

class LoadGameScreen(Screen):
    """The load game screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("enter", "load_selected_game", "Load", show=True),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        yield DataTable(id="load_game_table")
        yield Footer(show_command_palette=True)

    def on_mount(self):
        """Called when the screen is mounted."""
        table = self.query_one(DataTable)
        table.add_column("Save Slot", width=100)
        
        save_slots = get_save_slots()
        if save_slots:
            for slot in save_slots:
                table.add_row(slot)
        else:
            table.add_row("No save games found.")
        table.focus()

    def on_key(self, event: Key) -> None:
        """Handle key events."""
        if event.key == "enter":
            self.action_load_selected_game()

    def action_load_selected_game(self):
        """Load the currently highlighted save game."""
        logging.info("action_load_selected_game called.")
        from .world import WorldScreen # Local import to avoid circular dependency
        
        table = self.query_one(DataTable)
        row_key = table.cursor_row
        logging.info(f"Current cursor row: {row_key}")
        if row_key is None:
            logging.warning("No row selected, aborting load.")
            return
            
        save_name = table.get_cell_at((row_key, 0))
        logging.info(f"Attempting to load save game: '{save_name}'")
        
        # Prevent trying to load the "No save games found." message
        if save_name == "No save games found.":
            logging.warning("Attempted to load 'No save games found.' message.")
            return

        # Load the game state from the selected slot. This function now handles
        # loading the correct faction data and placing it in the GameState object.
        loaded_game_state = load_game(save_name)
        
        if loaded_game_state:
            logging.info(f"Successfully loaded game state for '{save_name}'. Switching to WorldScreen.")
            self.app.game_state = loaded_game_state
            self.app.world = World(seed=int(time.time()))
            self.app.switch_screen(WorldScreen())
            self.app.start_game_loop()
            self.app.trigger_initial_quest_cache()
        else:
            logging.error(f"Failed to load game state for '{save_name}'.")
