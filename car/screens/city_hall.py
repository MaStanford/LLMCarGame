import math
import logging
from functools import partial
from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button, LoadingIndicator
from textual.containers import Grid, Vertical
from textual.binding import Binding
from textual.message import Message
from ..widgets.dialog import Dialog
from ..logic.quest_logic import handle_quest_acceptance, complete_quest
from ..logic.llm_quest_generator import generate_quest_from_llm
from ..logic.faction_logic import get_conquest_quest
from ..logic.boss import check_challenge_conditions, spawn_faction_boss
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_city_faction, get_buildings_in_city, find_safe_spawn_point
from ..workers.city_hall_dialog_generator import generate_dialog_worker
from textual.worker import Worker, WorkerState

class QuestsLoaded(Message):
    """A message to indicate that quests have been loaded."""
    def __init__(self, quests: list) -> None:
        self.quests = quests
        super().__init__()

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
        self.current_city_faction = get_city_faction(gs.car_world_x, gs.car_world_y, gs.factions)
        
        logging.info(f"CityHallScreen mounted for city: {self.current_city_id}")

        turn_in_city_tuple = (grid_x, grid_y)
        if gs.current_quest and gs.current_quest.ready_to_turn_in and gs.current_quest.city_id == turn_in_city_tuple:
            self.is_turn_in = True
        else:
            self.is_turn_in = False
            cached_quests = gs.quest_cache.get(self.current_city_id)
            if cached_quests is None:
                logging.info("No quests in cache. Generating new quests.")
                self.generate_quests()
            elif cached_quests == "pending":
                logging.info("Quests are currently being generated.")
            else:
                logging.info(f"Found {len(cached_quests)} quests in cache.")
                self.available_quests = cached_quests
            self.can_challenge = check_challenge_conditions(gs, self.current_city_faction, gs.factions)
        
        self.update_quest_display()
        self.generate_dialog()

    def on_quests_loaded(self, message: QuestsLoaded) -> None:
        """Handle the QuestsLoaded message."""
        logging.info(f"CityHallScreen received QuestsLoaded message with {len(message.quests)} quests.")
        self.available_quests = message.quests or []
        self.update_quest_display()

    def generate_dialog(self):
        """Starts a worker to generate shopkeeper dialog."""
        gs = self.app.game_state
        faction_info = gs.factions.get(self.current_city_faction, {})
        faction_name = faction_info.get("name", "The Wasteland")
        faction_vibe = faction_info.get("description", "A desolate, lawless place.")
        player_rep = gs.faction_reputation.get(self.current_city_faction, 0)

        worker_callable = partial(
            generate_dialog_worker,
            app=self.app,
            theme=gs.theme,
            faction_name=faction_name,
            faction_vibe=faction_vibe,
            player_reputation=player_rep
        )
        self.run_worker(worker_callable, exclusive=True, name="CityHallDialogGenerator", thread=True)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle completed dialog worker."""
        logging.info(f"Worker {event.worker.name} changed state to {event.worker.state}")
        if event.worker.name == "CityHallDialogGenerator":
            if event.worker.state == WorkerState.SUCCESS:
                dialog = event.worker.result
                self.query_one(Dialog).update(dialog)
            elif event.worker.state == WorkerState.ERROR:
                logging.error(f"CityHallDialogGenerator worker failed: {event.worker.error}")
        elif event.worker.name.startswith("QuestGenerator"):
            if event.worker.state == WorkerState.SUCCESS:
                quests = event.worker.result
                logging.info(f"QuestGenerator worker succeeded with result: {quests}")
                self.app.game_state.quest_cache[self.current_city_id] = quests or []
                self.post_message(QuestsLoaded(quests or []))
            else:
                logging.error(f"QuestGenerator worker failed with state: {event.worker.state}")
                self.app.game_state.quest_cache.pop(self.current_city_id, None)
                self.post_message(QuestsLoaded([]))

    def on_unmount(self) -> None:
        """Called when the screen is unmounted."""
        gs = self.app.game_state
        gs.menu_open = False

        grid_x = round(gs.car_world_x / CITY_SPACING)
        grid_y = round(gs.car_world_y / CITY_SPACING)
        buildings = get_buildings_in_city(grid_x, grid_y)
        
        current_building = next((b for b in buildings if b.get("type") == "city_hall"), None)
        
        if current_building:
            exit_x = current_building['x'] + current_building['w'] / 2
            exit_y = current_building['y'] + current_building['h'] + 2
            
            safe_x, safe_y = find_safe_spawn_point(exit_x, exit_y, buildings, gs.player_car)

            gs.car_world_x = safe_x
            gs.car_world_y = safe_y
            gs.car_angle = math.pi * 1.5 # Face down (South)
            gs.player_car.x = gs.car_world_x
            gs.player_car.y = gs.car_world_y
            gs.player_car.angle = gs.car_angle

    def update_quest_display(self) -> None:
        """Update the quest display."""
        logging.info(f"Updating quest display. {len(self.available_quests)} quests available.")
        challenge_button = self.query_one("#challenge_boss", Button)
        challenge_button.display = self.can_challenge
        loading_container = self.query_one("#loading_container")
        quest_list_widget = self.query_one("#quest_list")

        if self.is_turn_in:
            loading_container.display = False
            quest_list_widget.display = True
            quest = self.app.game_state.current_quest
            quest_list_widget.update("Quest Complete!")
            self.query_one("#quest_info", Static).update(quest.name)
            self.query_one(Dialog).update(quest.completion_dialog)
            self.query_one("#accept_quest", Button).label = "Complete Quest"
        else:
            cached_quests = self.app.game_state.quest_cache.get(self.current_city_id)
            if cached_quests == "pending":
                loading_container.display = True
                quest_list_widget.display = False
                self.query_one("#quest_info", Static).update("")
                self.query_one(Dialog).update("Checking the local job board...")
                self.query_one("#accept_quest", Button).disabled = True
            elif not self.available_quests:
                loading_container.display = False
                quest_list_widget.display = True
                quest_list_widget.update("No contracts available at this time.")
                self.query_one("#quest_info", Static).update("")
                self.query_one(Dialog).update("Seems quiet around here...")
                self.query_one("#accept_quest", Button).disabled = True
            else:
                loading_container.display = False
                quest_list_widget.display = True
                quest_list_str = ""
                for i, quest in enumerate(self.available_quests):
                    quest_list_str += f"> {quest.name}\n" if i == self.selected_index else f"  {quest.name}\n"
                quest_list_widget.update(quest_list_str)
                
                selected_quest = self.available_quests[self.selected_index]
                self.query_one("#quest_info", Static).update(selected_quest.description)
                self.query_one(Dialog).update(selected_quest.dialog)
                self.query_one("#accept_quest", Button).disabled = False

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
            with Vertical(id="quest_list_container"):
                with Vertical(id="loading_container"):
                    yield LoadingIndicator()
                    yield Static("Contacting the Mayor for contracts...", id="loading_label")
                yield Static("Available Contracts", id="quest_list")
            yield Static("Quest Details", id="quest_info")
            yield Dialog("")
            with Vertical():
                yield Button("Accept", id="accept_quest", variant="primary")
                yield Button("Challenge Faction Leader", id="challenge_boss", variant="error")
        yield Footer(show_command_palette=True)
