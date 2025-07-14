from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.containers import Vertical

class CityHallScreen(ModalScreen):
    """A modal screen for the city hall."""

    def __init__(self, game_state) -> None:
        self.game_state = game_state
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="city-hall-dialog"):
            yield Static("City Hall", id="city-hall-title")
            # We'll populate quests dynamically later
            yield Button("View Quests", id="view-quests")
            yield Button("Back", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "view-quests":
            # In a real scenario, we'd fetch and display a list of quests.
            # For now, we'll just show a placeholder briefing.
            from ..logic.quests import QUESTS
            quest = list(QUESTS.values())[0] # Get a sample quest
            self.app.push_screen(QuestBriefingScreen(quest))

class QuestBriefingScreen(ModalScreen):
    """A modal screen for the quest briefing."""

    def __init__(self, quest) -> None:
        self.quest = quest
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="quest-briefing-dialog"):
            yield Static("Contract Briefing", id="quest-briefing-title")
            yield Static(f"GIVER: {self.quest.quest_giver_faction}")
            yield Static(f"TARGET: {self.quest.target_faction}")
            yield Static("OBJECTIVE:")
            yield Static(self.quest.description)
            yield Static("REWARDS:")
            yield Static(f"- Cash: {self.quest.rewards['cash']}")
            yield Static(f"- XP: {self.quest.rewards['xp']}")
            yield Static("CONSEQUENCES:")
            yield Static(f"- {self.quest.quest_giver_faction} Reputation: +10")
            yield Static(f"- {self.quest.target_faction} Reputation: -15")
            yield Button("Accept Contract", variant="primary", id="accept")
            yield Button("Decline", variant="error", id="decline")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "accept":
            # Here we would add the quest to the player's state
            self.app.pop_screen()
            self.app.pop_screen() # Also pop CityHallScreen
        elif event.button.id == "decline":
            self.app.pop_screen()
