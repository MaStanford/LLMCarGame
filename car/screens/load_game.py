from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable
from textual.binding import Binding
from ..logic.save_load import get_save_slots, load_game
from ..logic.data_loader import load_faction_data
import importlib

class LoadGameScreen(Screen):
    """The load game screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("enter", "load_selected_game", "Load"),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        yield DataTable(id="load_game_table")
        yield Footer()

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

    def action_load_selected_game(self):
        """Load the currently highlighted save game."""
        from ..app import WorldScreen # Local import to avoid circular dependency
        
        table = self.query_one(DataTable)
        row_key = table.cursor_row
        if row_key is None:
            return
            
        save_name = table.get_cell_at((row_key, 0))
        
        # Load the game state from the selected slot
        loaded_game_state = load_game(save_name)
        
        if loaded_game_state:
            # IMPORTANT: Reload the faction data to ensure the session uses the loaded data
            importlib.reload(self.app.data.factions)
            self.app.data.factions.FACTION_DATA = load_faction_data()
            
            self.app.game_state = loaded_game_state
            self.app.switch_screen(WorldScreen())
            self.app.game_loop = self.app.set_interval(1 / 30, self.app.update_game)
