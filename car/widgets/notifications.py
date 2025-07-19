from textual.widgets import Static
import time

class Notifications(Static):
    can_focus = False
    """A widget to display notifications."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.notifications = []

    def add_notification(self, text: str, duration: int = 3) -> None:
        self.notifications.append({
            "text": text,
            "duration": duration,
            "start_time": time.time()
        })
        self.update()

    def on_update(self) -> None:
        self.notifications = [
            n for n in self.notifications
            if time.time() - n["start_time"] < n["duration"]
        ]
        self.update_render()

    def render(self) -> str:
        return "\n".join(n["text"] for n in self.notifications)

