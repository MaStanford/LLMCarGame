from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable

class LoadGameScreen(Screen):
    """The load game screen."""

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        yield DataTable()
        yield Footer()
