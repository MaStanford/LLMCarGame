import math
import logging
import time

from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Horizontal, Vertical, Container

from ..data.game_constants import CITY_SPACING
from ..widgets.entity_modal import EntityModal
from ..widgets.explosion import Explosion
from ..widgets.hud_stats import StatsHUD
from ..widgets.hud_location import HudLocation
from ..widgets.hud_compass import CompassHUD
from ..widgets.hud_quest import QuestHUD
from ..widgets.hud_weapons import WeaponHUD
from ..widgets.game_view import GameView
from ..widgets.notifications import Notifications
from ..widgets.fps_counter import FPSCounter
from ..world.generation import get_city_name
from ..logic.spawning import spawn_initial_entities
from ..logic.debug_commands import execute_command
from ..widgets.debug_console import DebugConsole
from .inventory import InventoryScreen
from .pause_menu import PauseScreen
from .map import MapScreen
from .faction import FactionScreen
from .quest_detail import QuestDetailScreen

from textual.events import Key
from textual.binding import Binding

# --- Input Constants ---
# Keys that are tracked for continuous (hold-to-act) input.
# These are handled via on_key + staleness expiry, NOT Textual bindings,
# so that multiple gameplay keys can be held simultaneously.
GAMEPLAY_KEYS = {"w", "s", "a", "d", "space", "left", "right"}
KEY_STALE_THRESHOLD = 0.15  # seconds — if no repeat event arrives within this window, the key is considered released
PEDAL_RAMP_RATE = 4.0       # pedal units per second (0 to 1.0 in ~0.25s)

class WorldScreen(Screen):
    """The default screen for the game."""

    _pressed_keys: dict = {}  # key_name -> last_event_timestamp (reset in on_mount)

    # Only one-shot menu/UI keys use Textual bindings.
    # Gameplay keys (WASD, space, arrows) are handled by on_key + process_input.
    # They are listed here with show=True purely so the footer displays them as hints.
    BINDINGS = [
        Binding("w", "noop", "Accelerate", show=True),
        Binding("s", "noop", "Brake", show=True),
        Binding("a", "noop", "Turn Left", show=True),
        Binding("d", "noop", "Turn Right", show=True),
        Binding("left", "noop", "Aim Left", show=True),
        Binding("right", "noop", "Aim Right", show=True),
        Binding("space", "noop", "Fire", show=True),
        Binding("1", "toggle_weapon(1)", "Wpn 1", show=False),
        Binding("2", "toggle_weapon(2)", "Wpn 2", show=False),
        Binding("3", "toggle_weapon(3)", "Wpn 3", show=False),
        Binding("4", "toggle_weapon(4)", "Wpn 4", show=False),
        Binding("5", "toggle_weapon(5)", "Wpn 5", show=False),
        Binding("6", "toggle_weapon(6)", "Wpn 6", show=False),
        Binding("7", "toggle_weapon(7)", "Wpn 7", show=False),
        Binding("8", "toggle_weapon(8)", "Wpn 8", show=False),
        Binding("9", "toggle_weapon(9)", "Wpn 9", show=False),
        Binding("escape", "toggle_pause", "Pause", show=True),
        Binding("tab", "toggle_inventory", "Inventory", show=False),
        Binding("i", "toggle_inventory", "Inventory", show=True),
        Binding("m", "show_map", "Map", show=True),
        Binding("f", "show_factions", "Factions", show=True),
        Binding("q", "show_quests", "Quests", show=True),
        Binding("enter", "show_notifications", "Show Log", show=False),
        Binding("grave_accent", "toggle_console", "Console", show=False),
        Binding("tilde", "toggle_console", "~ Console", show=False),
    ]

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._pressed_keys = {}  # key_name -> last_event_timestamp
        self.focus()
        gs = self.app.game_state

        # Synchronize the player car's entity position with the game state's world position
        gs.player_car.x = gs.car_world_x
        gs.player_car.y = gs.car_world_y

        # Spawn an initial batch of entities
        spawn_initial_entities(gs, self.app.world)

        # Hide FPS counter if not in dev mode
        if not self.app.dev_mode:
            self.query_one("#fps_counter").display = False

    def on_screen_resume(self) -> None:
        """Called when the screen is resumed."""
        self._pressed_keys = {}  # Clear stale keys from before the menu
        self.app.game_state.pause_menu_open = False
        self.app.game_state.menu_open = False
        self.app.start_game_loop()

        # Update FPS counter visibility in case Dev Mode changed
        fps_counter = self.query_one("#fps_counter")
        if fps_counter:
            fps_counter.display = self.app.dev_mode

    def on_key(self, event: Key) -> None:
        """Track gameplay keys for continuous input (hold-to-act).

        Textual has no key-up events. Instead, we record the timestamp of each
        key-repeat event. The game loop's process_input() expires keys that
        haven't received a repeat within KEY_STALE_THRESHOLD, treating that
        as a key release.
        """
        if event.key in GAMEPLAY_KEYS:
            self._pressed_keys[event.key] = time.time()

    def process_input(self, dt: float) -> None:
        """Called each game tick to translate held keys into game actions.

        This replaces the old per-key Textual binding actions for gameplay keys.
        All gameplay keys can now be held simultaneously.
        """
        gs = self.app.game_state
        now = time.time()

        # Expire stale keys (no repeat event within threshold = key released)
        self._pressed_keys = {
            k: t for k, t in self._pressed_keys.items()
            if now - t < KEY_STALE_THRESHOLD
        }

        # --- Turning (continuous, dt-scaled via vehicle_movement.py) ---
        gs.actions["turn_left"] = "a" in self._pressed_keys
        gs.actions["turn_right"] = "d" in self._pressed_keys

        # --- Throttle / Brake (ramp while held, sticky on release) ---
        if "w" in self._pressed_keys:
            gs.pedal_position = min(1.0, gs.pedal_position + PEDAL_RAMP_RATE * dt)
        if "s" in self._pressed_keys:
            gs.pedal_position = max(-1.0, gs.pedal_position - PEDAL_RAMP_RATE * dt)

        # --- Firing (continuous while held, gated by weapon cooldowns) ---
        gs.actions["fire"] = "space" in self._pressed_keys

        # --- Weapon Aiming (continuous swivel, stat-based) ---
        if "left" in self._pressed_keys:
            gs.weapon_angle_offset -= gs.weapon_aim_speed * dt
        if "right" in self._pressed_keys:
            gs.weapon_angle_offset += gs.weapon_aim_speed * dt

    # --- One-shot menu actions (still use Textual bindings) ---

    def action_noop(self) -> None:
        """No-op action for gameplay keys displayed in footer.
        Actual input is handled by on_key + process_input."""
        pass

    def action_toggle_weapon(self, slot: int) -> None:
        """Toggle weapon on/off by slot number (1-indexed)."""
        gs = self.app.game_state
        point_names = list(gs.mounted_weapons.keys())
        idx = slot - 1
        if idx < 0 or idx >= len(point_names):
            return
        point_name = point_names[idx]
        current = gs.weapon_enabled.get(point_name, True)
        gs.weapon_enabled[point_name] = not current
        weapon = gs.mounted_weapons.get(point_name)
        weapon_label = weapon.name if weapon else "Empty"
        state = "ON" if not current else "OFF"
        notifications = self.query_one("#notifications", Notifications)
        notifications.add_notification(f"[{slot}] {weapon_label}: {state}")

    def action_toggle_pause(self) -> None:
        """Toggle the pause menu."""
        if self.app.game_state.pause_menu_open:
            self.app.pop_screen()
        else:
            self.app.stop_game_loop()
            self.app.game_state.pause_menu_open = True
            self.app.push_screen(PauseScreen())

    def action_toggle_inventory(self) -> None:
        """Toggle the inventory screen."""
        if self.app.game_state.menu_open:
            self.app.pop_screen()
        else:
            self.app.game_state.menu_open = True
            self.app.push_screen(InventoryScreen())

    def action_show_map(self) -> None:
        """Pushes the map screen."""
        self.app.stop_game_loop()
        self.app.push_screen(MapScreen())

    def action_show_factions(self) -> None:
        """Pushes the faction screen."""
        self.app.push_screen(FactionScreen())

    def action_show_quests(self) -> None:
        """Pushes the quest detail screen."""
        self.app.push_screen(QuestDetailScreen())

    def action_show_notifications(self) -> None:
        """Re-show recent notification history."""
        self.query_one("#notifications", Notifications).show_history()

    def action_toggle_console(self) -> None:
        """Toggle the debug console (dev mode only)."""
        if not self.app.dev_mode:
            self.notify("Console requires dev mode", severity="warning")
            return
        existing = self.query("#debug_console")
        if existing:
            existing.first().remove()
        else:
            self.mount(DebugConsole())
            self.notify("Debug console opened")

    def on_debug_console_command_submitted(self, event: DebugConsole.CommandSubmitted) -> None:
        """Handle a submitted debug command."""
        result = execute_command(self.app.game_state, self.app.world, event.command)
        notifications = self.query_one("#notifications", Notifications)
        for line in result.split("\n"):
            notifications.add_notification(line)

    def compose(self):
        """Compose the layout of the screen."""
        yield GameView(id="game_view", game_state=self.app.game_state, world=self.app.world)

        with Vertical(id="top_hud"):
            yield FPSCounter(id="fps_counter")
            yield HudLocation(id="location_hud")
            yield CompassHUD(id="compass_hud")
            yield Notifications(id="notifications")

        with Vertical(id="right_hud"):
            yield WeaponHUD(id="weapon_hud")
            yield Static("", id="right_spacer")
            yield EntityModal(id="entity_modal")

        with Horizontal(id="bottom_hud"):
            yield QuestHUD(id="quest_hud")
            yield StatsHUD(id="stats_hud")

        yield Footer(show_command_palette=True)

    def update_widgets(self):
        """Update the screen widgets."""
        game_view = self.query_one("#game_view", GameView)
        game_view.refresh()

        gs = self.app.game_state

        stats_hud = self.query_one("#stats_hud", StatsHUD)
        stats_hud.cash = gs.player_cash
        stats_hud.durability = int(gs.current_durability)
        stats_hud.max_durability = int(gs.max_durability)
        stats_hud.gas = gs.current_gas
        stats_hud.gas_capacity = int(gs.gas_capacity)
        stats_hud.speed = gs.car_speed
        stats_hud.level = gs.player_level
        stats_hud.xp = gs.current_xp
        stats_hud.xp_to_next_level = gs.xp_to_next_level
        stats_hud.pedal_position = gs.pedal_position

        # Update Weapon HUD
        weapon_hud = self.query_one("#weapon_hud", WeaponHUD)
        weapons_info = []
        for slot_idx, (point_name, weapon) in enumerate(gs.mounted_weapons.items(), start=1):
            point_data = gs.attachment_points.get(point_name, {})
            mount_label = point_data.get("name", point_name)
            enabled = gs.weapon_enabled.get(point_name, True)
            if weapon:
                weapons_info.append({
                    "mount_name": mount_label,
                    "weapon_name": weapon.name,
                    "ammo_type": weapon.ammo_type,
                    "ammo": gs.ammo_counts.get(weapon.ammo_type, 0),
                    "empty": False,
                    "enabled": enabled,
                    "slot": slot_idx,
                })
            else:
                weapons_info.append({
                    "mount_name": mount_label,
                    "weapon_name": "",
                    "ammo_type": "",
                    "ammo": 0,
                    "empty": True,
                    "enabled": enabled,
                    "slot": slot_idx,
                })
        weapon_hud.weapons_data = weapons_info

        quest_hud = self.query_one("#quest_hud", QuestHUD)
        quest_hud.quest_name = gs.current_quest.name if gs.current_quest else "None"

        location = self.query_one("#location_hud", HudLocation)
        location.x = int(gs.car_world_x)
        location.y = int(gs.car_world_y)
        grid_x = round(gs.car_world_x / CITY_SPACING)
        grid_y = round(gs.car_world_y / CITY_SPACING)
        location.city_name = get_city_name(grid_x, grid_y, gs.factions)

        compass = self.query_one("#compass_hud", CompassHUD)
        compass.target_angle = gs.compass_info["target_angle"]
        compass.player_angle = gs.compass_info["player_angle"]
        compass.target_name = gs.compass_info["target_name"]

        # Update Entity Modal (always visible)
        entity_modal = self.query_one("#entity_modal", EntityModal)
        closest_entity = gs.closest_entity_info
        if closest_entity:
            entity_modal.entity_name = closest_entity["name"]
            entity_modal.hp = closest_entity["hp"]
            entity_modal.max_hp = closest_entity["max_hp"]
            entity_modal.art = closest_entity["art"]
        else:
            entity_modal.entity_name = "No Target"
            entity_modal.hp = 0
            entity_modal.max_hp = 0
            entity_modal.art = []

        # Handle explosions
        for destroyed in gs.destroyed_this_frame:
            art = destroyed.art.get("N") if isinstance(destroyed.art, dict) else destroyed.art
            explosion = Explosion(art)
            self.mount(explosion)
            explosion.offset = (int(destroyed.x - gs.car_world_x + self.size.width / 2),
                                int(destroyed.y - gs.car_world_y + self.size.height / 2))
            # Show destruction feedback in entity modal
            if getattr(destroyed, "is_faction_boss", False) and hasattr(destroyed, "name"):
                entity_modal.destroyed_name = destroyed.name
            else:
                entity_modal.destroyed_name = destroyed.__class__.__name__.replace("_", " ").title()
            entity_modal.destroyed_timer = time.time()
        gs.destroyed_this_frame.clear()
