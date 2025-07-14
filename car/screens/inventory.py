from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static

class InventoryScreen(ModalScreen):
    """The inventory screen."""

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        yield Static("Car Preview", id="car_preview")
        yield Static("Attachments", id="attachments")
        yield Static("Inventory", id="inventory")
        yield Static("Stats", id="stats")
        yield Footer()
