from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button, Static
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.message import Message

class CycleWidget(Vertical):
    """A widget for cycling through a list of options."""

    DEFAULT_CSS = """
        CycleWidget {
            align-horizontal: center;
        }
        
        .cycle-widget-container {
            width: auto;
        }

        .cycle-label {
            text-align: center;
        }

        .cycle-controls-container {
            width: auto;
            height: auto;
            align: center middle;
        }

        .cycle-button {
            min-width: 5;
            width: auto;
        }

        .cycle-value {
            min-width: 15;
            width: auto;
            text-align: center;
            border: round white;
        }

        CycleWidget.focused .cycle-value {
            border: round yellow;
        }
    """

    class Changed(Message):
        """Posted when the value changes."""
        def __init__(self, value: str, control_id: str) -> None:
            self.value = value
            self.control_id = control_id
            super().__init__()

    options = reactive([])
    current_index = reactive(0)

    def __init__(self, label: str, options: list[str], initial_index: int = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.label = label
        self.options = options
        self.current_index = initial_index

    def compose(self) -> ComposeResult:
        with Vertical(classes="cycle-widget-container"):
            yield Static(self.label, classes="cycle-label")
            with Horizontal(classes="cycle-controls-container"):
                yield Button("<", id="previous", classes="cycle-button")
                yield Static(self.options[self.current_index], id="value-label", classes="cycle-value")
                yield Button(">", id="next", classes="cycle-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "previous":
            self.current_index = (self.current_index - 1 + len(self.options)) % len(self.options)
        elif event.button.id == "next":
            self.current_index = (self.current_index + 1) % len(self.options)
        
        self.query_one("#value-label", Static).update(self.options[self.current_index])
        self.post_message(self.Changed(self.options[self.current_index], self.id))
