from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid, Vertical
from textual.binding import Binding
from ..widgets.dialog import Dialog
from ..logic.quest_logic import get_available_quests, handle_quest_acceptance, complete_quest
from ..logic.boss import check_challenge_conditions, spawn_faction_boss
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_city_faction

class CityHallScreen(ModalScreen):
    """The city hall screen for accepting quests."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("up", "move_selection(-1)", "Up"),
        Binding("down", "move_selection(1)", "Down"),
    ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.available_quests = []
        self.selected_index = 0
        self.is_turn_in = False
        self.can_challenge = False
        self.current_city_faction = None

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        gs = self.app.game_state
        self.current_city_faction = get_city_faction(gs.car_world_x, gs.car_world_y)
        current_city_id = (round(gs.car_world_x / CITY_SPACING), round(gs.car_world_y / CITY_SPACING))
        
        if gs.current_quest and gs.current_quest.ready_to_turn_in and gs.current_quest.city_id == current_city_id:
            self.is_turn_in = True
        else:
            self.is_turn_in = False
            self.available_quests = get_available_quests(gs)
            self.can_challenge = check_challenge_conditions(gs, self.current_city_faction)
        
        self.update_quest_display()

    def update_quest_display(self) -> None:
        """Update the quest display."""
        challenge_button = self.query_one("#challenge_boss", Button)
        challenge_button.display = self.can_challenge

        if self.is_turn_in:
            quest = self.app.game_state.current_quest
            self.query_one("#quest_list", Static).update("Quest Complete!")
            self.query_one("#quest_info", Static).update(quest.name)
            self.query_one("#dialog_box", Dialog).update_text(quest.completion_dialog)
            self.query_one("#accept_quest", Button).label = "Complete Quest"
        else:
            # (Existing display logic)
            ...

    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the quest list."""
        if not self.is_turn_in:
            # This needs to be updated to handle the new button
            focusable = self.query("Button, Static#quest_list")
            # ... (logic to cycle focus)
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle accept button presses."""
        gs = self.app.game_state
        
        if event.button.id == "challenge_boss":
            spawn_faction_boss(gs, self.current_city_faction)
            self.app.screen.query_one("#notifications").add_notification(f"Challenge issued!")
            self.app.pop_screen()
            return

        if self.is_turn_in:
            # (Existing turn-in logic)
            ...
        else:
            # (Existing accept logic)
            ...

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="city_hall_grid"):
            yield Static("Available Contracts", id="quest_list")
            yield Static("Quest Details", id="quest_info")
            yield Dialog("", id="dialog_box")
            with Vertical():
                yield Button("Accept", id="accept_quest", variant="primary")
                yield Button("Challenge Faction Leader", id="challenge_boss", variant="error")
        yield Footer()
