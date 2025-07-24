from textual.widgets import Static

class MenuStatsHUD(Static):
    """A widget to display detailed player stats in menu screens."""

    def on_mount(self) -> None:
        """Called when the widget is mounted."""
        self.update_stats(self.app.game_state)

    def update_stats(self, gs) -> None:
        """Update the displayed stats."""
        if not gs:
            self.update("No game state available.")
            return
            
        ammo_str = "\n".join([f"- {ammo_type}: {count}" for ammo_type, count in gs.ammo_counts.items()])
        stats_str = f"""
[b]Quest:[/b] {gs.current_quest.name if gs.current_quest else 'None'}
[b]Level:[/b] {gs.player_level} (XP: {gs.current_xp}/{gs.xp_to_next_level})

[b]Durability:[/b] {gs.current_durability}/{gs.max_durability}
[b]Gas:[/b] {gs.current_gas:.0f}/{gs.gas_capacity}
[b]Cash:[/b] ${gs.player_cash}

[b]Ammo:[/b]
{ammo_str}
"""
        self.update(stats_str)
