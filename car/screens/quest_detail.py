from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static, Button
from textual.containers import Vertical, Horizontal
from textual.binding import Binding

from ..data.quests import (
    KillBossObjective, KillCountObjective, SurvivalObjective,
    DeliverPackageObjective, DefendLocationObjective,
)
from ..logic.quest_logic import get_quest_target_location


def _format_objective(obj):
    """Format a single objective into a human-readable status line."""
    status = "[green]Done[/green]" if obj.completed else "[yellow]Active[/yellow]"
    if isinstance(obj, KillBossObjective):
        return f"  {status}  Defeat {obj.boss_name}"
    elif isinstance(obj, KillCountObjective):
        return f"  {status}  Eliminate targets ({obj.kill_count}/{obj.target_count})"
    elif isinstance(obj, SurvivalObjective):
        remaining = max(0, obj.timer // 30)
        return f"  {status}  Survive ({remaining}s remaining)"
    elif isinstance(obj, DeliverPackageObjective):
        return f"  {status}  Deliver package to {obj.destination}"
    elif isinstance(obj, DefendLocationObjective):
        remaining = max(0, obj.timer // 30)
        return f"  {status}  Defend {obj.location} ({remaining}s remaining)"
    return f"  {status}  Unknown objective"


class QuestDetailScreen(ModalScreen):
    """A screen to display the details of the current quest."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._confirm_abandon = False

    def compose(self):
        """Compose the layout of the screen."""
        yield Header(show_clock=True)
        with Vertical(id="quest-detail-container"):
            yield Static(id="quest_title", classes="panel-title")
            yield Static(id="quest_description")
            yield Static(id="quest_objectives")
            yield Static(id="quest_rewards")
            with Horizontal(id="quest-buttons"):
                yield Button("Set to Compass", id="set_compass", variant="primary")
                yield Button("Abandon Quest", id="abandon_quest", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        quest = self.app.game_state.current_quest
        if quest:
            self.query_one("#quest_title", Static).update(f"[bold]{quest.name}[/bold]")
            self.query_one("#quest_description", Static).update(quest.description)

            # Objectives
            obj_lines = ["[bold]Objectives:[/bold]"]
            for obj in quest.objectives:
                obj_lines.append(_format_objective(obj))
            if quest.ready_to_turn_in:
                obj_lines.append("\n  [green]>> Return to city to turn in! <<[/green]")
            self.query_one("#quest_objectives", Static).update("\n".join(obj_lines))

            # Rewards
            rewards_lines = [
                "[bold]Rewards:[/bold]",
                f"  XP: {quest.rewards.get('xp', 0)}",
                f"  Cash: ${quest.rewards.get('cash', 0)}",
            ]
            self.query_one("#quest_rewards", Static).update("\n".join(rewards_lines))

            # Disable compass button if quest has no location
            qt_x, qt_y, _ = get_quest_target_location(quest, self.app.game_state)
            if qt_x is None:
                self.query_one("#set_compass", Button).disabled = True
        else:
            self.query_one("#quest_title", Static).update("No Active Quest")
            self.query_one("#quest_description", Static).update("")
            self.query_one("#quest_objectives", Static).update("")
            self.query_one("#quest_rewards", Static).update("")
            self.query_one("#set_compass", Button).disabled = True
            self.query_one("#abandon_quest", Button).disabled = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "set_compass":
            quest = self.app.game_state.current_quest
            if quest:
                qt_x, qt_y, qt_label = get_quest_target_location(quest, self.app.game_state)
                if qt_x is not None:
                    self.app.game_state.waypoint = {
                        "x": qt_x,
                        "y": qt_y,
                        "name": qt_label or quest.name,
                    }
                    self._notify(f"Compass set to: {qt_label or quest.name}")
                    self.app.pop_screen()

        elif event.button.id == "abandon_quest":
            if self._confirm_abandon:
                # Second press: actually abandon
                gs = self.app.game_state
                quest_name = gs.current_quest.name if gs.current_quest else "quest"
                gs.story_events.append({
                    "text": f"Abandoned '{quest_name}'.",
                    "event_type": "quest_failed",
                })
                gs.current_quest = None
                gs.waypoint = None
                self._notify("Quest Abandoned.")
                self.app.pop_screen()
            else:
                # First press: ask for confirmation
                self._confirm_abandon = True
                event.button.label = "Are you sure? (Press again)"

    def _notify(self, message: str):
        """Post a notification to the WorldScreen."""
        try:
            for screen in self.app.screen_stack:
                try:
                    notif = screen.query_one("#notifications")
                    notif.add_notification(message)
                    return
                except Exception:
                    continue
        except Exception:
            pass
