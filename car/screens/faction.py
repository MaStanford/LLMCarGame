from textual.screen import ModalScreen
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Grid
from textual.binding import Binding
from ..world.generation import get_city_name
from ..data.game_constants import CITY_SPACING
from ..logic.entity_loader import ALL_VEHICLES

class FactionScreen(ModalScreen):
    """A modal screen to display faction intelligence."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.faction_data = {}

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="faction_grid"):
            yield DataTable(id="faction_list")
            yield Static(id="faction_details")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        gs = self.app.game_state
        # Load the CURRENT session's faction data dynamically from the app
        self.faction_data = gs.factions
        
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_column("Faction", width=25)
        table.add_column("Control", width=15)
        table.add_column("Reputation", width=15)
        
        for faction_id, data in self.faction_data.items():
            control = gs.faction_control.get(faction_id, 50)
            reputation = gs.faction_reputation.get(faction_id, 0)
            table.add_row(data["name"], f"{control}%", str(reputation), key=faction_id)
            
        # Set initial focus and update details
        if table.row_count > 0:
            table.move_cursor(row=0, animate=False)
            initial_faction_name = table.get_row_at(0)[0]
            self.update_details(initial_faction_name)
        table.focus()

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Event handler for when a row is highlighted in the DataTable."""
        table = self.query_one(DataTable)
        faction_name = table.get_cell_at((event.cursor_row, 0))
        self.update_details(faction_name)

    def update_details(self, faction_name: str) -> None:
        """Update the faction detail panel."""
        gs = self.app.game_state
        details_panel = self.query_one("#faction_details")
        
        # Find the faction data
        faction_id = next((fid for fid, data in self.faction_data.items() if data["name"] == faction_name), None)
        if not faction_id:
            details_panel.update("Select a faction.")
            return
            
        faction_data = self.faction_data[faction_id]
        rep = gs.faction_reputation.get(faction_id, 0)
        control = gs.faction_control.get(faction_id, 50)
        
        hub_x, hub_y = faction_data["hub_city_coordinates"]
        grid_x = round(hub_x / CITY_SPACING)
        grid_y = round(hub_y / CITY_SPACING)
        capital_name = get_city_name(grid_x, grid_y, gs.factions)
        
        unit_names = []
        for unit_id in faction_data.get("units", []):
            vehicle_class = next((v for v in ALL_VEHICLES if v.__name__.lower() == unit_id.lower()), None)
            if vehicle_class:
                unit_names.append(vehicle_class(0,0).name)
            else:
                unit_names.append(unit_id.replace("_", " ").title())
        units_str = ", ".join(unit_names) if unit_names else "N/A"

        details = f"[bold]{faction_name}[/bold]\n\n"
        details += f"Capital: {capital_name}\n"
        details += f"Control: {control}%\n"
        details += f"Reputation: {rep}\n\n"
        details += f"[bold]Known Units:[/bold]\n{units_str}\n\n"
        details += "[bold]Relationships:[/bold]\n"
        for other_id, status in faction_data.get("relationships", {}).items():
            # Use the dynamically loaded faction data for lookup
            if other_id in self.faction_data:
                other_name = self.faction_data[other_id]["name"]
                details += f"- {other_name}: {status}\n"
            
        details_panel.update(details)
