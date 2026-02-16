from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid, Vertical
from ..logic.combat_logic import player_turn, enemy_turn, check_combat_end

class CombatScreen(ModalScreen):
    """The combat screen."""

    def __init__(self, player, enemy, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player = player
        self.enemy = enemy
        self.combat_log = []

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Grid(id="combat_grid"):
            with Vertical(id="player_panel"):
                yield Static(self.player.name)
                yield Static(id="player_art")
                yield Static(id="player_stats")
            with Vertical(id="enemy_panel"):
                yield Static(self.enemy.name)
                yield Static(id="enemy_art")
                yield Static(id="enemy_stats")
        with Grid(id="combat_actions"):
            yield Button("Fire Weapons", id="fire", variant="primary")
            yield Button("Use Ability", id="ability", variant="default", disabled=True)
            yield Button("Attempt to Flee", id="flee", variant="error")
        yield Static(id="combat_log")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.update_display()

    def update_display(self) -> None:
        """Update the display."""
        player_art = self.query_one("#player_art", Static)
        p_art = self.player.get_static_art()
        player_art.update("\n".join(p_art))

        player_stats = self.query_one("#player_stats", Static)
        player_stats.update(f"HP: {self.player.durability}/{self.player.max_durability}")

        enemy_art = self.query_one("#enemy_art", Static)
        e_art = self.enemy.get_static_art()
        enemy_art.update("\n".join(e_art))
        
        enemy_stats = self.query_one("#enemy_stats", Static)
        enemy_stats.update(f"HP: {self.enemy.durability}/{self.enemy.max_durability}")

        log_widget = self.query_one("#combat_log", Static)
        log_widget.update("\n".join(self.combat_log[-5:])) # Show last 5 log entries

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle combat action button presses."""
        log = player_turn(self.app.game_state, event.button.id)
        self.combat_log.extend(log)
        
        end_state = check_combat_end(self.app.game_state)
        if end_state:
            self.handle_combat_end(end_state)
            return

        log = enemy_turn(self.app.game_state)
        self.combat_log.extend(log)
        
        end_state = check_combat_end(self.app.game_state)
        if end_state:
            self.handle_combat_end(end_state)
            return
            
        self.update_display()

    def handle_combat_end(self, result: str):
        """Handle the end of combat."""
        if result == "victory":
            self.app.game_state.active_enemies.remove(self.enemy)
            # (Add XP and loot rewards)
            for screen in self.app.screen_stack:
                notifications = screen.query("#notifications")
                if notifications:
                    notifications.first().add_notification(f"You defeated the {self.enemy.name}!")
                    break
            self.app.game_state.menu_open = False
            self.app.pop_screen()
        elif result == "defeat":
            self.app.game_state.game_over = True
            self.app.pop_screen() # Pop combat so the main loop can push game over
