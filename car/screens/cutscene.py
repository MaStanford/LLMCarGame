from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

class CutsceneScreen(Screen):
    """A screen to display a cutscene."""

    def __init__(self, frames: list[list[str]], delay: float) -> None:
        self.frames = frames
        self.delay = delay
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(id="cutscene-content")

    async def on_mount(self) -> None:
        content = self.query_one("#cutscene-content", Static)
        for frame in self.frames:
            content.update("\n".join(frame))
            await asyncio.sleep(self.delay)
        self.app.pop_screen()
