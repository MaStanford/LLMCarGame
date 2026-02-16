from textual.widget import Widget
from rich.text import Text
from rich.style import Style
import random

# Explosion characters with associated colors (no emojis — terminal-safe)
_FIRE_CHARS = [
    ("*", Style(color="red", bold=True)),
    ("#", Style(color="rgb(255,100,0)", bold=True)),
    ("~", Style(color="rgb(255,165,0)")),
    ("+", Style(color="yellow", bold=True)),
    (".", Style(color="rgb(200,80,0)")),
]
_SMOKE_CHARS = [
    (".", Style(color="rgb(100,100,100)")),
    (":", Style(color="rgb(80,80,80)")),
]

class Explosion(Widget):
    """A widget to display an explosion animation using colored ANSI characters."""

    def __init__(self, art, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.art = [list(row) for row in art]
        self.art_styles = [[Style() for _ in row] for row in self.art]
        self.original_art = [row[:] for row in self.art]
        self.animation_step = 0
        self.total_steps = 10

    def on_mount(self) -> None:
        """Start the animation when the widget is mounted."""
        self.set_timer(0.05, self.update_animation)

    def update_animation(self) -> None:
        """Update the animation frame."""
        self.animation_step += 1
        if self.animation_step > self.total_steps:
            self.remove()
            return

        progress = self.animation_step / self.total_steps
        for r, row in enumerate(self.original_art):
            for c, char in enumerate(row):
                if char != ' ' and random.random() < progress:
                    if progress < 0.6:
                        # Early: fire
                        ch, st = random.choice(_FIRE_CHARS)
                    elif progress < 0.85:
                        # Mid: mix of fire and smoke
                        ch, st = random.choice(_FIRE_CHARS + _SMOKE_CHARS)
                    else:
                        # Late: mostly smoke and fade
                        ch, st = random.choice(_SMOKE_CHARS + [(" ", Style())])
                    self.art[r][c] = ch
                    self.art_styles[r][c] = st

        self.refresh()
        self.set_timer(0.05, self.update_animation)

    def render(self) -> Text:
        """Render the current state of the explosion."""
        text = Text()
        for r, row in enumerate(self.art):
            for c, char in enumerate(row):
                text.append(char, self.art_styles[r][c])
            text.append("\n")
        return text
