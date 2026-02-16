from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Grid, Vertical
from ..logic.combat_logic import player_turn, enemy_turn, check_combat_end, get_current_phase

class CombatScreen(ModalScreen):
    """Turn-based boss combat screen with telegraph-and-counter mechanics."""

    def __init__(self, player, enemy, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.player = player
        self.enemy = enemy
        self.combat_log = []

    def compose(self):
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
        yield Static(id="phase_display")
        with Grid(id="combat_actions"):
            yield Button("Fire Weapons", id="fire", variant="primary")
            yield Button("Defend", id="defend", variant="default")
            yield Button("Evade", id="evade", variant="warning")
            yield Button("Flee", id="flee", variant="error")
        yield Static(id="combat_log")
        yield Footer()

    def on_mount(self) -> None:
        gs = self.app.game_state
        # Sync player HP from game_state into player entity for display
        self.player.durability = gs.current_durability
        self.player.max_durability = gs.max_durability
        # Show initial telegraph
        phase = get_current_phase(gs)
        self.combat_log.append(f"The {self.enemy.name} {phase['telegraph']}")
        self.update_display()

    def update_display(self) -> None:
        gs = self.app.game_state

        # Player art and stats
        player_art = self.query_one("#player_art", Static)
        p_art = self.player.get_static_art()
        player_art.update("\n".join(p_art))

        player_stats = self.query_one("#player_stats", Static)
        player_stats.update(f"HP: {gs.current_durability}/{gs.max_durability}")

        # Enemy art and stats
        enemy_art = self.query_one("#enemy_art", Static)
        e_art = self.enemy.get_static_art()
        enemy_art.update("\n".join(e_art))

        enemy_stats = self.query_one("#enemy_stats", Static)
        enemy_stats.update(f"HP: {self.enemy.durability}/{self.enemy.max_durability}")

        # Boss phase telegraph
        phase = get_current_phase(gs)
        phase_widget = self.query_one("#phase_display", Static)
        phase_widget.update(
            f"═══ {phase['name'].upper()} ═══\n"
            f"The {self.enemy.name} {phase['telegraph']}\n"
            f"Tip: {phase['tip']}"
        )

        # Combat log (last 6 entries)
        log_widget = self.query_one("#combat_log", Static)
        log_widget.update("\n".join(self.combat_log[-6:]))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        gs = self.app.game_state
        log, fled = player_turn(gs, event.button.id)
        self.combat_log.extend(log)

        if fled:
            # Successful flee — skip enemy turn, sync HP, pop screen
            gs.current_durability = max(0, gs.current_durability)
            self.app.pop_screen()
            return

        end_state = check_combat_end(gs)
        if end_state:
            self.handle_combat_end(end_state)
            return

        log = enemy_turn(gs)
        self.combat_log.extend(log)

        end_state = check_combat_end(gs)
        if end_state:
            self.handle_combat_end(end_state)
            return

        self.update_display()

    def handle_combat_end(self, result: str):
        gs = self.app.game_state
        if result == "victory":
            # Grant rewards
            xp = getattr(self.enemy, 'xp_value', 50)
            cash = getattr(self.enemy, 'cash_value', 100)
            gs.gain_xp(xp)
            gs.player_cash += cash
            self.combat_log.append(f"Victory! +{xp} XP, +{cash} cash")

            # Remove enemy from world
            if self.enemy in gs.active_enemies:
                gs.active_enemies.remove(self.enemy)

            # Handle faction boss defeat
            if getattr(self.enemy, 'is_faction_boss', False):
                from ..logic.boss import handle_faction_boss_defeat
                handle_faction_boss_defeat(gs, self.enemy)

            # Notify
            for screen in self.app.screen_stack:
                notifications = screen.query("#notifications")
                if notifications:
                    notifications.first().add_notification(f"You defeated the {self.enemy.name}!")
                    break

            gs.menu_open = False
            self.app.pop_screen()
        elif result == "defeat":
            gs.game_over = True
            self.app.pop_screen()
