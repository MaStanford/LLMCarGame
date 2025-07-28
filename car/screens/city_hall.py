import math
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid, Vertical
from textual.binding import Binding
from ..widgets.dialog import Dialog
from ..logic.quest_logic import handle_quest_acceptance, complete_quest
from ..logic.llm_quest_generator import generate_quest_from_llm
from ..logic.faction_logic import get_conquest_quest
from ..logic.boss import check_challenge_conditions, spawn_faction_boss
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_city_faction, get_buildings_in_city

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
        self.current_city_id = None

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        gs = self.app.game_state
        grid_x = round(gs.car_world_x / CITY_SPACING)
        grid_y = round(gs.car_world_y / CITY_SPACING)
        self.current_city_id = f"city_{grid_x}_{grid_y}"
        self.current_city_faction = get_city_faction(gs.car_world_x, gs.car_world_y)
        
        # Check for quest turn-in
        turn_in_city_tuple = (grid_x, grid_y)
        if gs.current_quest and gs.current_quest.ready_to_turn_in and gs.current_quest.city_id == turn_in_city_tuple:
            self.is_turn_in = True
        else:
            self.is_turn_in = False
            
            # Check for a high-stakes conquest quest first
            conquest_quest = get_conquest_quest(gs)
            if conquest_quest and conquest_quest.quest_giver_faction == self.current_city_faction:
                self.available_quests = [conquest_quest]
            else:
                # --- Quest Pre-fetching Logic ---
                cached_quests = gs.quest_cache.get(self.current_city_id)
                if cached_quests == "pending":
                    self.available_quests = [] # Show loading state
                elif cached_quests:
                    self.available_quests = cached_quests
                else:
                    # This should rarely happen if the caching is working, but as a fallback:
                    logging.warning(f"No quests found in cache for {self.current_city_id}. Caching may be slow.")
                    self.available_quests = []

            self.can_challenge = check_challenge_conditions(gs, self.current_city_faction)
        
        self.update_quest_display()

    def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        gs = self.app.game_state
        gs.menu_open = False

        # Find the building the player is in
        grid_x = round(gs.car_world_x / CITY_SPACING)
        grid_y = round(gs.car_world_y / CITY_SPACING)
        buildings = get_buildings_in_city(grid_x, grid_y)
        
        current_building = None
        for building in buildings:
            if (building['x'] <= gs.car_world_x < building['x'] + building['w'] and
                building['y'] <= gs.car_world_y < building['y'] + building['h']):
                current_building = building
                break
        
        # If found, move the player just outside of it
        if current_building:
            gs.car_world_x = current_building['x'] + current_building['w'] / 2
            gs.car_world_y = current_building['y'] + current_building['h'] + 2 # Place below
            gs.car_angle = math.pi * 1.5 # Face down (South)
            gs.player_car.x = gs.car_world_x
            gs.player_car.y = gs.car_world_y
            gs.player_car.angle = gs.car_angle

    def update_quest_display(self) -> None:
        """Update the quest display."""
        challenge_button = self.query_one("#challenge_boss", Button)
        challenge_button.display = self.can_challenge

        if self.is_turn_in:
            quest = self.app.game_state.current_quest
            self.query_one("#quest_list", Static).update("Quest Complete!")
            self.query_one("#quest_info", Static).update(quest.name)
            self.query_one(Dialog).update_text(quest.completion_dialog)
            self.query_one("#accept_quest", Button).label = "Complete Quest"
        else:
            quest_list_str = ""
            if not self.available_quests:
                cached_quests = self.app.game_state.quest_cache.get(self.current_city_id)
                if cached_quests == "pending":
                    quest_list_str = "Checking for new contracts..."
                else:
                    quest_list_str = "No contracts available at this time."
                self.query_one("#quest_info", Static).update("")
                self.query_one(Dialog).update_text("Seems quiet around here...")
                self.query_one("#accept_quest", Button).disabled = True
            else:
                for i, quest in enumerate(self.available_quests):
                    if i == self.selected_index:
                        quest_list_str += f"> {quest.name}\n"
                    else:
                        quest_list_str += f"  {quest.name}\n"
                
                selected_quest = self.available_quests[self.selected_index]
                self.query_one("#quest_info", Static).update(selected_quest.description)
                self.query_one(Dialog).update(selected_quest.dialog)
                self.query_one("#accept_quest", Button).disabled = False

            self.query_one("#quest_list", Static).update(quest_list_str)


    def action_move_selection(self, amount: int) -> None:
        """Move the selection in the quest list."""
        if not self.is_turn_in and self.available_quests:
            self.selected_index = (self.selected_index + amount + len(self.available_quests)) % len(self.available_quests)
            self.update_quest_display()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle accept button presses."""
        gs = self.app.game_state
        
        if event.button.id == "challenge_boss":
            spawn_faction_boss(gs, self.current_city_faction)
            self.app.screen.query_one("#notifications").add_notification(f"Challenge issued!")
            self.app.pop_screen()
            return

        if self.is_turn_in:
            complete_quest(gs, self.app)
            self.app.pop_screen()
        else:
            if self.available_quests:
                selected_quest = self.available_quests[self.selected_index]
                handle_quest_acceptance(gs, selected_quest)
                # Clear the cache for this city now that a quest has been taken
                if self.current_city_id in gs.quest_cache:
                    del gs.quest_cache[self.current_city_id]
                self.app.pop_screen()

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="city_hall_grid"):
            yield Static("Available Contracts", id="quest_list")
            yield Static("Quest Details", id="quest_info")
            yield Dialog("")
            with Vertical():
                yield Button("Accept", id="accept_quest", variant="primary")
                yield Button("Challenge Faction Leader", id="challenge_boss", variant="error")
        yield Footer()
