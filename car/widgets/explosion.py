from textual.widget import Widget
from rich.text import Text
import random

class Explosion(Widget):
    """A widget to display an explosion animation."""

    def __init__(self, art, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.art = [list(row) for row in art]
        self.original_art = [row[:] for row in self.art]
        self.animation_step = 0
        self.total_steps = 10 # Number of frames in the explosion

    def on_mount(self) -> None:
        """Start the animation when the widget is mounted."""
        self.set_timer(0.05, self.update_animation)

    def update_animation(self) -> None:
        """Update the animation frame."""
        self.animation_step += 1
        if self.animation_step > self.total_steps:
            self.remove()
            return

        # Randomly replace characters with explosion symbols
        for r, row in enumerate(self.original_art):
            for c, char in enumerate(row):
                if char != ' ' and random.random() < (self.animation_step / self.total_steps):
                    self.art[r][c] = random.choice(["*", "💥", "🔥", " "])
        
        self.refresh()
        self.set_timer(0.05, self.update_animation)

    def render(self) -> Text:
        """Render the current state of the explosion."""
        text = Text()
        for row in self.art:
            text.append("".join(row) + "\n")
        return text
