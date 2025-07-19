from textual.widgets import Static
from textual.reactive import reactive

class FPSCounter(Static):
    can_focus = False
    """A widget to display the current FPS."""
    
    fps = reactive(0.0)

    def watch_fps(self, new_fps: float) -> None:
        """Called when the fps reactive attribute changes."""
        self.update(f"FPS: {new_fps:.2f}")

