from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid
from textual.binding import Binding
from ..widgets.dialog import Dialog
from ..logic.quest_logic import get_available_quests, handle_quest_acceptance, complete_quest
from ..data.game_constants import CITY_SPACING

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

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        gs = self.app.game_state
        current_city_id = (round(gs.car_world_x / CITY_SPACING), round(gs.car_world_y / CITY_SPACING))
        
        if gs.current_quest and gs.current_quest.ready_to_turn_in and gs.current_quest.city_id == current_city_id:
            self.is_turn_in = True
        else:
            self.is_turn_in = False
            self.available_quests = get_available_quests(gs)
        
        self.update_quest_display()

    def update_quest_display(self) -> None:
        """Update the quest display."""
        if self.is_turn_in:
            quest = self.app.game_state.current_quest
            self.query_one("#quest_list", Static).update("Quest Complete!")
            self.query_one("#quest_info", Static).update(quest.name)
            self.query_one("#dialog_box", Dialog).update_text(quest.completion_dialog)
            self.query_one("#accept_quest", Button).label = "Complete Quest"
        else:
            # Quest List
            quest_list = self.query_one("#quest_list", Static)
            list_str = ""
            for i, quest in enumerate(self.available_quests):
                if i == self.selected_index:
                    list_str += f"> {quest.name}\n"
                else:
                    list_str += f"  {quest.name}\n"
            quest_list.update(list_str)

            # Quest Info and Dialog
            if self.available_quests:
                selected_quest = self.available_quests[self.selected_index]
                quest_info = self.query_one("#quest_info", Static)
                info_str = f"""
                {selected_quest.name}

                Rewards:
                - XP: {selected_quest.rewards.get("xp", 0)}
                - Cash: ${selected_quest.rewards.get("cash", 0)}
                """
                quest_info.update(info_str)
                
                dialog = self.query_one("#dialog_box", Dialog)
                dialog.update_text(selected_quest.offer_dialog)

    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the quest list."""
        if not self.is_turn_in:
            self.selected_index = (self.selected_index + amount + len(self.available_quests)) % len(self.available_quests)
            self.update_quest_display()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle accept button presses."""
        if self.is_turn_in:
            complete_quest(self.app.game_state)
            self.app.screen.query_one("#notifications").add_notification("Quest Complete!")
            self.app.pop_screen()
        else:
            if self.available_quests:
                selected_quest = self.available_quests[self.selected_index]
                handle_quest_acceptance(self.app.game_state, selected_quest)
                self.app.screen.query_one("#notifications").add_notification(f"New Quest: {selected_quest.name}")
                self.app.pop_screen()

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="city_hall_grid"):
            yield Static("Available Contracts", id="quest_list")
            yield Static("Quest Details", id="quest_info")
            yield Dialog("", id="dialog_box")
            yield Button("Accept", id="accept_quest", variant="primary")
        yield Footer()