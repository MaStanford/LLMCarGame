from textual.widgets import Static
from textual.containers import Horizontal

class Controls(Static):
    """A widget to display the game controls."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.renderable = ""

    def on_mount(self) -> None:
        with self.mount(Horizontal()):
            self.mount(Static("WASD: Steer", classes="control-item"))
            self.mount(Static("SPACE: Fire", classes="control-item"))
            self.mount(Static("ESC: Pause", classes="control-item"))
