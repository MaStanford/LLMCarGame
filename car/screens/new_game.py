import logging
from textual.app import ComposeResult
from textual.containers import Vertical, Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer
from textual.binding import Binding

from .theme_selection import ThemeSelectionScreen
from ..widgets.item_info import ItemInfoWidget
from ..widgets.cycle_widget import CycleWidget
from ..logic.entity_loader import PLAYER_CARS
from ..data.difficulty import DIFFICULTY_LEVELS, DIFFICULTY_MODIFIERS
from ..data.colors import CAR_COLORS
from ..entities.weapon import Weapon


class NewGameScreen(Screen):
    """The new game setup screen."""

    BINDINGS = [
        Binding("up", "focus_previous", "Up"),
        Binding("down", "focus_next", "Down"),
        Binding("left", "cycle_left", "Left"),
        Binding("right", "cycle_right", "Right"),
        Binding("a", "rotate_left", "Rotate Left"),
        Binding("d", "rotate_right", "Rotate Right"),
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focusable_widgets = []
        self.current_focus_index = 0

    def compose(self) -> ComposeResult:
        """Compose the layout of the screen."""
        yield Header(show_clock=True, name="New Game")
        with Vertical(id="new-game-container"):
            with Horizontal(id="new-game-layout"):
                # --- LEFT COLUMN ---
                with Vertical(id="new-game-left-column"):
                    with Vertical(id="car-preview-container"):
                        yield Static(id="car-preview")
                    yield Static("Default Weapons", classes="panel-title")
                    with Vertical(id="weapon-list-container", classes="focusable"):
                        yield Static(id="weapon_list")
                    yield ItemInfoWidget(id="item_info")

                # --- RIGHT COLUMN ---
                with Vertical(id="new-game-right-column"):
                    with Vertical(classes="cycle-widgets-container"):
                        yield CycleWidget(
                            label="Car",
                            options=[car.__name__ for car in PLAYER_CARS],
                            id="car_select",
                        )
                        yield CycleWidget(
                            label="Color",
                            options=list(CAR_COLORS.keys()),
                            id="color_select",
                        )
                        yield CycleWidget(
                            label="Difficulty",
                            options=DIFFICULTY_LEVELS,
                            initial_index=1,
                            id="difficulty_select",
                        )
                    yield Button("Start Game", id="start_game", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the initial state of the screen."""
        self.selected_car_index = 0
        self.selected_color_name = self.query_one("#color_select", CycleWidget).options[0]
        self.selected_weapon_index = 0
        self.preview_angle = 0
        
        self.focusable_widgets = [
            self.query_one("#car_select", CycleWidget),
            self.query_one("#color_select", CycleWidget),
            self.query_one("#difficulty_select", CycleWidget),
            self.query_one("#weapon-list-container"),
            self.query_one("#start_game", Button),
        ]
        
        self.current_focus_index = 0
        self.update_focus()
        self.update_car_and_weapon_info()

    def update_focus(self) -> None:
        """Update the visual and native focus state."""
        for i, widget in enumerate(self.focusable_widgets):
            if i == self.current_focus_index:
                widget.add_class("focused")
                widget.focus()
            else:
                widget.remove_class("focused")

    def action_focus_previous(self) -> None:
        """Focus the previous widget in our custom list."""
        self.current_focus_index = (self.current_focus_index - 1 + len(self.focusable_widgets)) % len(self.focusable_widgets)
        self.update_focus()
        self.update_weapon_focus()

    def action_focus_next(self) -> None:
        """Focus the next widget in our custom list."""
        self.current_focus_index = (self.current_focus_index + 1) % len(self.focusable_widgets)
        self.update_focus()
        self.update_weapon_focus()

    def action_cycle_left(self) -> None:
        """Cycle the focused widget to the left, or change selected weapon."""
        focused_widget = self.focusable_widgets[self.current_focus_index]
        if isinstance(focused_widget, CycleWidget):
            focused_widget.query_one("#previous", Button).press()
        elif focused_widget.id == "weapon-list-container":
            self.selected_weapon_index -=1
            self.update_car_and_weapon_info()

    def action_cycle_right(self) -> None:
        """Cycle the focused widget to the right, or change selected weapon."""
        focused_widget = self.focusable_widgets[self.current_focus_index]
        if isinstance(focused_widget, CycleWidget):
            focused_widget.query_one("#next", Button).press()
        elif focused_widget.id == "weapon-list-container":
            self.selected_weapon_index +=1
            self.update_car_and_weapon_info()

    def action_rotate_left(self) -> None:
        """Rotate the car preview counterclockwise."""
        self.preview_angle = (self.preview_angle - 45) % 360
        self.update_car_and_weapon_info()

    def action_rotate_right(self) -> None:
        """Rotate the car preview clockwise."""
        self.preview_angle = (self.preview_angle + 45) % 360
        self.update_car_and_weapon_info()
    
    def update_weapon_focus(self):
        """Visual update for weapon list focus."""
        weapon_container = self.query_one("#weapon-list-container")
        if self.focusable_widgets[self.current_focus_index] == weapon_container:
            weapon_container.border_title = "Weapons (Selected)"
        else:
            weapon_container.border_title = ""
        self.update_car_and_weapon_info()

    def on_cycle_widget_changed(self, event: CycleWidget.Changed) -> None:
        """Handle changes from the cycle widgets."""
        if event.control_id == "car_select":
            self.selected_car_index = self.query_one("#car_select", CycleWidget).current_index
            self.selected_weapon_index = 0
            self.update_car_and_weapon_info()
        elif event.control_id == "color_select":
            self.selected_color_name = event.value
            self.update_car_and_weapon_info()

    def get_art_for_angle(self, car_instance, angle):
        """Gets the correct vehicle art for a given angle."""
        if isinstance(car_instance.art, dict):
            angle = angle % 360
            if 337.5 <= angle or angle < 22.5: direction = "N"
            elif 22.5 <= angle < 67.5: direction = "NE"
            elif 67.5 <= angle < 112.5: direction = "E"
            elif 112.5 <= angle < 157.5: direction = "SE"
            elif 157.5 <= angle < 202.5: direction = "S"
            elif 202.5 <= angle < 247.5: direction = "SW"
            elif 247.5 <= angle < 292.5: direction = "W"
            else: direction = "NW"
            art = car_instance.art.get(direction, [""])
        else:
            art = car_instance.art
        return "\n".join(art)

    def update_car_and_weapon_info(self) -> None:
        """Update the car preview and weapon list."""
        car_class = PLAYER_CARS[self.selected_car_index]
        car_instance = car_class(x=0, y=0)
        
        color_style = CAR_COLORS[self.selected_color_name]
        color = color_style.color.name if color_style.color else "white"
        
        # Handle both dict (directional) and list (non-directional) art
        if isinstance(car_instance.art, dict):
            art_dict = car_instance.art
        else:
            art_dict = {"N": car_instance.art} # Fallback for non-directional

        # Get the art for the current angle
        if isinstance(car_instance.art, dict):
            art_lines = self.get_art_for_angle(car_instance, self.preview_angle).split("\n")
        else:
            art_lines = car_instance.art

        art = "\n".join(art_lines)
        self.query_one("#car-preview", Static).update(f"[{color}]{art}[/]")

        color_widget = self.query_one("#color_select", CycleWidget)
        color_name = self.selected_color_name.replace("CAR_", "").replace("_", " ").title()
        color_widget.query_one(".cycle-value").update(color_name)
        color_widget.query_one(".cycle-value").styles.color = color

        weapon_list = self.query_one("#weapon_list", Static)
        item_info = self.query_one("#item_info", ItemInfoWidget)

        if hasattr(car_instance, "default_weapons"):
            weapons = [Weapon(w) for w in car_instance.default_weapons.values()]
            if not weapons:
                weapon_list.update("No weapons.")
                item_info.display_item(None)
                return

            self.selected_weapon_index = self.selected_weapon_index % len(weapons)
            weapon_list_str = ""
            for i, weapon in enumerate(weapons):
                if i == self.selected_weapon_index:
                    weapon_list_str += f"> {weapon.name}\n"
                    item_info.display_item(weapon)
                else:
                    weapon_list_str += f"  {weapon.name}\n"
            weapon_list.update(weapon_list_str)
        else:
            weapon_list.update("No weapons.")
            item_info.display_item(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "start_game":
            difficulty = self.query_one("#difficulty_select", CycleWidget).options[self.query_one("#difficulty_select", CycleWidget).current_index]
            color_name = self.query_one("#color_select", CycleWidget).options[self.query_one("#color_select", CycleWidget).current_index]

            settings = {
                "selected_car_index": self.selected_car_index,
                "difficulty": difficulty,
                "difficulty_mods": DIFFICULTY_MODIFIERS[difficulty],
                "car_color_name": color_name,
            }

            if getattr(self.app, "dev_quick_start", False):
                self._quick_start(settings)
            else:
                self.app.switch_screen(ThemeSelectionScreen(settings))

    def _quick_start(self, new_game_settings: dict) -> None:
        """Skip all LLM generation and start immediately with fallback data."""
        import time
        import os
        import shutil
        import pprint
        import json
        import logging

        from ..game_state import GameState
        from ..world import World
        from ..logic.llm_theme_generator import _get_fallback_themes
        from ..logic.llm_faction_generator import _get_fallback_factions
        from ..logic.llm_quest_generator import _get_fallback_quest
        from ..logic.save_load import load_triggers
        from ..world.generation import get_buildings_in_city, find_safe_spawn_point

        logging.info("Dev Quick Start: skipping LLM generation, using fallback data.")

        # Use fallback data for everything
        theme = _get_fallback_themes()[0]
        factions = _get_fallback_factions()
        new_game_settings["theme"] = theme

        # Find neutral faction at (0,0)
        neutral_faction_id = next(
            (fid for fid, data in factions.items()
             if data.get("hub_city_coordinates") == [0, 0]),
            list(factions.keys())[0]
        )

        # Generate fallback quests
        quests = []
        for _ in range(3):
            q = _get_fallback_quest(neutral_faction_id)
            if q:
                quests.append(q)

        # Build world details from faction hubs
        cities = {}
        for fid, fdata in factions.items():
            if "hub_city_coordinates" in fdata:
                coords = fdata["hub_city_coordinates"]
                cities[f"{coords[0]},{coords[1]}"] = f"The City of {fdata['name']}"
        world_details = {"cities": cities, "roads": [], "landmarks": []}

        story_intro = (
            "You arrive at the neutral city of The Junction, a beacon of tense "
            "neutrality in a world torn apart by warring factions. Your goal is "
            "simple: find the Genesis Module and escape. Good luck."
        )

        # Save factions to temp/ (same as WorldBuildingScreen.start_game)
        if os.path.exists("temp"):
            shutil.rmtree("temp")
        os.makedirs("temp")
        with open("temp/factions.py", "w") as f:
            f.write("FACTION_DATA = ")
            pprint.pprint(factions, stream=f, indent=4)
        with open("temp/world_details.json", "w") as f:
            json.dump(world_details, f, indent=4)

        self.app.reload_dynamic_data()

        # Create game state
        game_state = GameState(
            selected_car_index=new_game_settings["selected_car_index"],
            difficulty=new_game_settings["difficulty"],
            difficulty_mods=new_game_settings["difficulty_mods"],
            car_color_names=[new_game_settings["car_color_name"]],
            theme=theme,
            factions=factions,
        )
        game_state.world_details = world_details
        game_state.story_intro = story_intro
        game_state.quest_cache[f"city_0_0"] = quests

        load_triggers(game_state)

        # Spawn at neutral city (0, 0)
        buildings = get_buildings_in_city(0, 0)
        safe_x, safe_y = find_safe_spawn_point(0.0, 0.0, buildings, game_state.player_car, max_radius=100)
        game_state.car_world_x = safe_x
        game_state.car_world_y = safe_y
        game_state.player_car.x = safe_x
        game_state.player_car.y = safe_y

        self.app.game_state = game_state
        self.app.world = World(seed=int(time.time()))

        # Go directly to the world screen
        from ..screens.world import WorldScreen
        self.app.start_game_loop()
        self.app.switch_screen(WorldScreen())

