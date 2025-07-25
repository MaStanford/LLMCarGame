import json
import logging
from .prompt_builder import build_quest_prompt
from ..data.quests import Quest

def generate_quest_from_llm(game_state, quest_giver_faction_id, pipeline):
    """
    Generates a new quest by calling the language model.
    """
    if pipeline is None or pipeline == "unavailable":
        logging.warning("LLM pipeline not available. Using fallback quest.")
        return _get_fallback_quest(quest_giver_faction_id)

    prompt = build_quest_prompt(game_state)
    messages = [{"role": "user", "content": prompt}]

    try:
        outputs = pipeline(
            messages,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.8,
        )
        quest_json_str = outputs[0]["generated_text"][-1]["content"]
        
        cleaned_json = quest_json_str.strip().replace("```json", "").replace("```", "")
        quest_data = json.loads(cleaned_json)
        
        # TODO: Dynamically select target faction based on context
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
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        logging.error(f"Error parsing LLM output for quests: {e}")
        return _get_fallback_quest(quest_giver_faction_id)
    except Exception as e:
        logging.error(f"Error during LLM generation: {e}", exc_info=True)
        return _get_fallback_quest(quest_giver_faction_id)

def _get_fallback_quest(quest_giver_faction_id):
    """Returns a hardcoded fallback quest for testing."""
    return Quest(
        name="Fallback: Scrap Metal Mayhem",
        description="Raid a scrap yard and destroy a war rig.",
        dialog="The Vultures are getting too bold. Go destroy their war rig.",
        objectives=[["KillBossObjective", ["Scrap King Klaw"]]],
        rewards={"xp": 500, "cash": 1000},
        quest_giver_faction=quest_giver_faction_id,
        target_faction="the_vultures",
    )