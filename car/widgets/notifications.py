from textual.widgets import Static
import time

MAX_VISIBLE = 5
MAX_HISTORY = 20


class Notifications(Static):
    """A widget to display notifications with queue and history support."""
    can_focus = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.notifications = []
        self.history = []

    def add_notification(self, text: str, duration: int = 3) -> None:
        entry = {
            "text": text,
            "duration": duration,
            "start_time": time.time(),
        }
        self.notifications.append(entry)
        self.history.append({"text": text})
        # Cap history
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]
        # Cap visible notifications
        if len(self.notifications) > MAX_VISIBLE:
            self.notifications = self.notifications[-MAX_VISIBLE:]
        self.update()

    def show_history(self) -> None:
        """Re-show recent history entries with fresh timestamps."""
        now = time.time()
        recent = self.history[-MAX_VISIBLE:]
        self.notifications = [
            {"text": n["text"], "duration": 3, "start_time": now}
            for n in recent
        ]
        self.update()

    def on_update(self) -> None:
        self.notifications = [
            n for n in self.notifications
            if time.time() - n["start_time"] < n["duration"]
        ]
        self.update_render()

    def render(self) -> str:
        if not self.notifications:
            return ""
        return "\n".join(n["text"] for n in self.notifications)
