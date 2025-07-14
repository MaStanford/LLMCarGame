from textual.app import ComposeResult
from textual.containers import Vertical, Container
from textual.screen import Screen
from textual.widgets import Button, Static, Header, Footer
from textual.binding import Binding

from ..widgets.weapon_info import WeaponInfo
from ..widgets.cycle_widget import CycleWidget
from ..logic.entity_loader import PLAYER_CARS
from ..data.difficulty import DIFFICULTY_LEVELS, DIFFICULTY_MODIFIERS
from ..data.colors import COLOR_PAIRS_DEFS
from ..game_state import GameState
from ..app import DefaultScreen
from ..entities.weapon import Weapon
from ..world import World


class NewGameScreen(Screen):
    """The new game setup screen."""

    BINDINGS = [
        Binding("up", "focus_previous", "Up"),
        Binding("down", "focus_next", "Down"),
        Binding("left", "cycle_left", "Left"),
        Binding("right", "cycle_right", "Right"),
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.focusable_widgets = []
        self.current_focus_index = 0

    def compose(self) -> ComposeResult:
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Container(id="new-game-scroll-container"):
            with Vertical(id="new-game-container"):
                with Vertical(id="car-preview-container"):
                    yield Static(id="car-preview")
                with Vertical(classes="cycle-widgets-container"):
                    yield CycleWidget(
                        label="Car",
                        options=[car.__name__ for car in PLAYER_CARS],
                        id="car_select",
                    )
                    yield CycleWidget(
                        label="Color",
                        options=[name for name in COLOR_PAIRS_DEFS if name.startswith("CAR_")],
                        id="color_select",
                    )
                    yield CycleWidget(
                        label="Difficulty",
                        options=DIFFICULTY_LEVELS,
                        initial_index=1,
                        id="difficulty_select",
                    )
                yield Static("Weapons", classes="panel-title")
                with Vertical(id="weapon-list-container", classes="focusable"):
                    yield Static(id="weapon_list")
                yield WeaponInfo(id="weapon_info")
                yield Button("Start Game", id="start_game", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Set up the initial state of the screen."""
        self.selected_car_index = 0
        self.selected_color_name = self.query_one("#color_select", CycleWidget).options[0]
        self.selected_weapon_index = 0
        self.preview_angle = 0
        
        # Custom Focus Management:
        # Textual's default focus system wasn't providing the fine-grained
        # control needed for this screen's layout. To solve this, we implement
        # a manual focus system.
        # 1. A list, `focusable_widgets`, defines the exact order of navigation.
        # 2. The `current_focus_index` tracks the currently "focused" widget.
        # 3. `action_focus_next` and `action_focus_previous` handle changing this
        #    index when the user presses up/down.
        # 4. The `update_focus` method is called to apply a `.focused` CSS
        #    class to the widget at the current index and remove it from others.
        # 5. CSS rules in `app.css` then use this `.focused` class to apply
        #    visual styling (e.g., `CycleWidget.focused .cycle-value`).
        # This approach gives us complete control over the tab order and visual
        # feedback without interfering with Textual's internal focus state.
        self.focusable_widgets = [
            self.query_one("#car_select", CycleWidget),
            self.query_one("#color_select", CycleWidget),
            self.query_one("#difficulty_select", CycleWidget),
            self.query_one("#weapon-list-container"),
            self.query_one("#start_game", Button),
        ]
        
        self.current_focus_index = 0
        self.update_focus()
        self.update_car_info()

    def update_focus(self) -> None:
        """Update the visual and native focus state."""
        for i, widget in enumerate(self.focusable_widgets):
            if i == self.current_focus_index:
                widget.add_class("focused")
                widget.focus()  # Set native focus
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
            self.update_car_info()


    def action_cycle_right(self) -> None:
        """Cycle the focused widget to the right, or change selected weapon."""
        focused_widget = self.focusable_widgets[self.current_focus_index]
        if isinstance(focused_widget, CycleWidget):
            focused_widget.query_one("#next", Button).press()
        elif focused_widget.id == "weapon-list-container":
            self.selected_weapon_index +=1
            self.update_car_info()
    
    def update_weapon_focus(self):
        """Visual update for weapon list focus."""
        weapon_container = self.query_one("#weapon-list-container")
        if self.focusable_widgets[self.current_focus_index] == weapon_container:
            weapon_container.border_title = "Weapons (Selected)"
        else:
            weapon_container.border_title = ""
        self.update_car_info()

    def on_cycle_widget_changed(self, event: CycleWidget.Changed) -> None:
        """Handle changes from the cycle widgets."""
        if event.control_id == "car_select":
            self.selected_car_index = self.query_one("#car_select", CycleWidget).current_index
            self.selected_weapon_index = 0
            self.update_car_info()
        elif event.control_id == "color_select":
            self.selected_color_name = event.value
            self.update_car_info()


    def get_art_for_angle(self, car_instance, angle):
        """Gets the correct vehicle art for a given angle."""
        if isinstance(car_instance.art, dict):
            angle = angle % 360
            if 337.5 <= angle or angle < 22.5:
                direction = "N"
            elif 22.5 <= angle < 67.5:
                direction = "NE"
            elif 67.5 <= angle < 112.5:
                direction = "E"
            elif 112.5 <= angle < 157.5:
                direction = "SE"
            elif 157.5 <= angle < 202.5:
                direction = "S"
            elif 202.5 <= angle < 247.5:
                direction = "SW"
            elif 247.5 <= angle < 292.5:
                direction = "W"
            else:
                direction = "NW"
            art = car_instance.art.get(direction, [""])
        else:
            art = car_instance.art
        return "\n".join(art)

    def update_car_info(self) -> None:
        """Update the car preview and weapon list."""
        car_class = PLAYER_CARS[self.selected_car_index]
        car_instance = car_class(x=0, y=0)
        
        # Apply color to the art
        color = self.selected_color_name.lower().replace("car_", "")
        colored_art_dict = {}
        for direction, art_lines in car_instance.art.items():
            colored_art_dict[direction] = [f"[{color}]{line}[/]" for line in art_lines]
        car_instance.art = colored_art_dict

        art = self.get_art_for_angle(car_instance, self.preview_angle)
        self.query_one("#car-preview", Static).update(art)

        # Update color widget text
        color_widget = self.query_one("#color_select", CycleWidget)
        color_name = self.selected_color_name.replace("CAR_", "").replace("_", " ").title()
        color_widget.query_one(".cycle-value").update(color_name)
        color_widget.query_one(".cycle-value").styles.color = color

        weapon_list = self.query_one("#weapon_list", Static)
        weapon_info = self.query_one("#weapon_info", WeaponInfo)

        if hasattr(car_instance, "default_weapons"):
            weapons = [
                Weapon(w) for w in car_instance.default_weapons.values()
            ]
            if not weapons:
                weapon_list.update("No weapons.")
                weapon_info.name = "N/A"
                weapon_info.damage = 0
                weapon_info.range = 0
                weapon_info.fire_rate = 0
                return

            self.selected_weapon_index = self.selected_weapon_index % len(weapons)
            weapon_list_str = ""
            for i, weapon in enumerate(weapons):
                if i == self.selected_weapon_index:
                    weapon_list_str += f"> {weapon.name}\n"
                    weapon_info.name = weapon.name
                    weapon_info.damage = weapon.damage
                    weapon_info.range = weapon.range
                    weapon_info.fire_rate = weapon.fire_rate
                else:
                    weapon_list_str += f"  {weapon.name}\n"
            weapon_list.update(weapon_list_str)
        else:
            weapon_list.update("No weapons.")
            weapon_info.name = "N/A"
            weapon_info.damage = 0
            weapon_info.range = 0
            weapon_info.fire_rate = 0

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "start_game":
            difficulty = self.query_one("#difficulty_select", CycleWidget).options[self.query_one("#difficulty_select", CycleWidget).current_index]
            color_name = self.query_one("#color_select", CycleWidget).options[self.query_one("#color_select", CycleWidget).current_index]
            
            self.app.game_state = GameState(
                selected_car_index=self.selected_car_index,
                difficulty=difficulty,
                difficulty_mods=DIFFICULTY_MODIFIERS[difficulty],
                car_color_names=[color_name],
                car_color_pair_num=COLOR_PAIRS_DEFS[color_name]["id"],
            )
            self.app.world = World(seed=12345)
            self.app.switch_screen(DefaultScreen())
            self.app.set_interval(1 / 30, self.app.update_game)
