import json
# from llama_cpp import Llama

from ..logic.data_loader import FACTION_DATA
from ..data.quests import Quest
from .prompt_builder import build_quest_prompt

def generate_quest_from_llm(game_state, quest_giver_faction_id):
    """
    Generates a new quest by calling a local LLM with a dynamically built prompt.
    """
    
    # --- 1. Assemble the Prompt ---
    prompt = build_quest_prompt(game_state)

    # --- 2. Call the LLM (Placeholder) ---
    # llm = Llama(model_path="./path/to/your/model.gguf")
    # response = llm(prompt, max_tokens=1024, stop=["```"], echo=False)
    # quest_json_str = response["choices"][0]["text"]
    
    # For now, use a hardcoded fallback response for testing
    quest_json_str = """
{
  "name": "Scrap Metal Mayhem",
  "description": "Raid the Vultures' scrap yard and destroy their prized war rig.",
  "dialog": "The Vultures are getting too bold. We need to send them a message. Go to their main scrap yard and turn their 'invincible' war rig into a pile of junk. That should get their attention.",
  "objectives": [
    ["KillBossObjective", ["Scrap King Klaw"]]
  ],
  "rewards": {
    "xp": 500,
    "cash": 1000
  }
}
    """

    # --- 3. Parse and Return ---
    try:
        quest_data = json.loads(quest_json_str)
        # TODO: Add validation and dynamically select target faction
        target_faction_id = "the_vultures" 
        
        return Quest(
            name=quest_data["name"],
            description=quest_data["description"],
            dialog=quest_data["dialog"],
            objectives=quest_data["objectives"],
            rewards=quest_data["rewards"],
            quest_giver_faction=quest_giver_faction_id,
            target_faction=target_faction_id,
        )
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing LLM output for quests: {e}")
        return None # Return None on failure

