from textual.screen import ModalScreen
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Grid
from textual.binding import Binding
from ..logic.data_loader import FACTION_DATA

class FactionScreen(ModalScreen):
    """A modal screen to display faction intelligence."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="faction_grid"):
            yield DataTable(id="faction_list")
            yield Static(id="faction_details", content_align="center")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        gs = self.app.game_state
        
        # --- Faction List Table ---
        table = self.query_one(DataTable)
        table.add_column("Faction", width=30)
        table.add_column("Control", width=20)
        
        for faction_id, data in FACTION_DATA.items():
            control = gs.faction_control.get(faction_id, "N/A")
            table.add_row(data["name"], f"{control}%")
            
        # --- Initial Detail View ---
        self.update_details()
        
        # --- Listen for cursor changes ---
        self.query_one(DataTable).watch("cursor_row", self.update_details)

    def update_details(self, *args) -> None:
        """Update the faction detail panel."""
        gs = self.app.game_state
        table = self.query_one(DataTable)
        details_panel = self.query_one("#faction_details")
        
        if table.cursor_row < 0:
            details_panel.update("")
            return
            
        faction_name = table.get_cell_at((table.cursor_row, 0))
        
        # Find the faction data
        faction_id = next((fid for fid, data in FACTION_DATA.items() if data["name"] == faction_name), None)
        if not faction_id:
            details_panel.update("Select a faction.")
            return
            
        faction_data = FACTION_DATA[faction_id]
        rep = gs.faction_reputation.get(faction_id, 0)
        
        # --- Build the details string ---
        details = f"[bold]{faction_name}[/bold]\n\n"
        details += f"Reputation: {rep}\n\n"
        details += "[bold]Relationships:[/bold]\n"
        for other_id, status in faction_data["relationships"].items():
            other_name = FACTION_DATA[other_id]["name"]
            details += f"- {other_name}: {status}\n"
            
        details_panel.update(details)
