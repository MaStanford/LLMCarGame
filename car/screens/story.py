from textual.screen import ModalScreen
from textual.widgets import Header, Footer, Static
from textual.containers import VerticalScroll
from textual.binding import Binding


class StoryScreen(ModalScreen):
    """A journal screen that shows the full narrative history of the game."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
    ]

    def compose(self):
        yield Header(show_clock=True)
        with VerticalScroll(id="story-scroll"):
            yield Static(id="story_title")
            yield Static(id="story_theme")
            yield Static(id="story_intro")
            yield Static(id="story_chronicle")
            yield Static(id="story_current")
            yield Static(id="story_world_state")
        yield Footer()

    def on_mount(self) -> None:
        gs = self.app.game_state

        # --- Title ---
        self.query_one("#story_title", Static).update(
            "[bold]THE STORY SO FAR[/bold]"
        )

        # --- Theme ---
        theme = gs.theme or {}
        theme_name = theme.get("name", "Unknown")
        theme_desc = theme.get("description", "")
        theme_text = f"[bold]Theme:[/bold] {theme_name}\n{theme_desc}" if theme_desc else f"[bold]Theme:[/bold] {theme_name}"
        self.query_one("#story_theme", Static).update(theme_text)

        # --- Prologue ---
        intro = gs.story_intro or "No prologue recorded."
        self.query_one("#story_intro", Static).update(
            f"[bold]Prologue[/bold]\n{intro}"
        )

        # --- Chronicle ---
        events = getattr(gs, "story_events", [])
        if events:
            lines = []
            event_icons = {
                "quest_complete": "+",
                "quest_failed": "x",
                "boss_defeated": "*",
                "faction_takeover": "!",
                "discovery": "?",
            }
            for ev in events:
                icon = event_icons.get(ev.get("event_type", ""), "-")
                lines.append(f"  [{icon}] {ev['text']}")
            chronicle_text = "[bold]Chronicle[/bold]\n" + "\n".join(lines)
        else:
            chronicle_text = "[bold]Chronicle[/bold]\nNo events recorded yet."
        self.query_one("#story_chronicle", Static).update(chronicle_text)

        # --- Current Quest ---
        if gs.current_quest:
            quest = gs.current_quest
            status = "Ready to turn in" if quest.ready_to_turn_in else "In Progress"
            quest_text = f"[bold]Current Quest[/bold]\n  {quest.name} ({status})\n  {quest.description}"
        else:
            quest_text = "[bold]Current Quest[/bold]\n  None"
        self.query_one("#story_current", Static).update(quest_text)

        # --- World State ---
        world_lines = ["[bold]World State[/bold]"]
        for faction_id, faction_data in gs.factions.items():
            name = faction_data["name"]
            rep = gs.faction_reputation.get(faction_id, 0)
            control = gs.faction_control.get(faction_id, 50)
            defeated = faction_id in gs.defeated_bosses
            boss_info = ""
            if defeated:
                boss_info = " (Boss Defeated)"
            world_lines.append(f"  {name}: Rep {rep:+d} | Control {control}%{boss_info}")
        self.query_one("#story_world_state", Static).update("\n".join(world_lines))
