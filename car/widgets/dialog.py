from textual.widgets import Static
from textual.containers import Vertical

class Dialog(Static):
    """A dialog widget."""

    def __init__(self, text_lines: list[str]) -> None:
        self.text_lines = text_lines
        super().__init__()

    def compose(self):
        with Vertical(id="dialog-box"):
            for line in self.text_lines:
                yield Static(line)
