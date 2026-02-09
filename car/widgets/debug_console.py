"""Debug console widget for the WorldScreen."""
from textual.widgets import Input
from textual.message import Message


class DebugConsole(Input):
    """A command-line input for debug commands. Mounted on WorldScreen when toggled."""

    class CommandSubmitted(Message):
        """Posted when the user submits a command."""
        def __init__(self, command: str) -> None:
            super().__init__()
            self.command = command

    def __init__(self) -> None:
        super().__init__(placeholder="Enter debug command...", id="debug_console")

    def on_mount(self) -> None:
        self.focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Forward the command to the parent screen."""
        if event.value.strip():
            self.post_message(self.CommandSubmitted(event.value.strip()))
        self.remove()

    def on_key(self, event) -> None:
        """Close on escape."""
        if event.key == "escape":
            self.remove()
            event.stop()
