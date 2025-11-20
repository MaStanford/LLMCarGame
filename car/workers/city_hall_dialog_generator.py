import logging
from textual.worker import Worker
from ..logic.gemini_cli import generate_with_gemini_cli
from ..logic import build_city_hall_dialog_prompt

class CityHallDialogWorker(Worker):
    def __init__(self, app, theme: str, faction_name: str, faction_vibe: str, player_reputation: int) -> None:
        super().__init__()
        self.app = app
        self.theme = theme
        self.faction_name = faction_name
        self.faction_vibe = faction_vibe
        self.player_reputation = player_reputation

    def action(self) -> str:
        """Generates dialog for the shopkeeper."""
        try:
            prompt = build_city_hall_dialog_prompt(
                theme=self.theme,
                faction_name=self.faction_name,
                faction_vibe=self.faction_vibe,
                player_reputation=self.player_reputation
            )
            
            if self.app.generation_mode == "gemini_cli":
                dialog = generate_with_gemini_cli(prompt, parse_json=False)
            else:
                # Fallback for local mode
                if self.player_reputation > 50:
                    dialog = "Welcome back, friend. Good to see you."
                elif self.player_reputation < -20:
                    dialog = "I'm watching you. Don't try anything funny."
                else:
                    dialog = "State your business."
            
            return dialog.strip()
        except Exception as e:
            logging.error(f"Error in CityHallDialogWorker: {e}", exc_info=True)
            return "Welcome, traveler."

def generate_dialog_worker(app, theme, faction_name, faction_vibe, player_reputation):
    """Callable for running the worker."""
    return CityHallDialogWorker(app, theme, faction_name, faction_vibe, player_reputation).action()
