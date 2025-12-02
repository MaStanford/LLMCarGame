import asyncio
from car.app import GenesisModuleApp
from car.game_state import GameState
from car.logic.prompt_builder import build_quest_prompt
from car.data.difficulty import DIFFICULTY_MODIFIERS
from car.data.factions import FACTION_DATA

async def main():
    """
    Initializes a game state and builds a sample quest prompt.
    """
    app = GenesisModuleApp()
    async with app.run_test() as pilot:
        # Provide default values to construct a valid GameState
        game_state = GameState(
            selected_car_index=0,
            difficulty="Normal",
            difficulty_mods=DIFFICULTY_MODIFIERS["Normal"],
            car_color_names=["CAR_RED"],
            factions=FACTION_DATA
        )

        # Pick a faction to be the quest giver
        # The default factions are loaded from car/data/factions.py
        quest_giver_faction_id = list(game_state.factions.keys())[0]
        
        print(f"--- Generating prompt for faction: {quest_giver_faction_id} ---")

        # Build the prompt
        prompt = build_quest_prompt(game_state, quest_giver_faction_id)

        # Print the result
        print("\n--- BUILT QUEST PROMPT ---")
        print(prompt)
        print("--------------------------")

if __name__ == "__main__":
    asyncio.run(main())
