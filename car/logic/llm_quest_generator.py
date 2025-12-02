import os
import json
import logging
import random
from .prompt_builder import build_quest_prompt
from ..data.quests import Quest
from .gemini_cli import generate_with_gemini_cli

def generate_quest_from_llm(game_state, quest_giver_faction_id, app, faction_data=None):
    """
    Generates a new quest by calling the language model.
    Can be passed faction_data directly to override the global data, useful for workers.
    """
    prompt = build_quest_prompt(game_state, quest_giver_faction_id, faction_data)
    
    if app.generation_mode == "gemini_cli":
        quest_data = generate_with_gemini_cli(prompt)
    else:
        # Local pipeline logic
        if app.llm_pipeline is None or app.llm_pipeline == "unavailable":
            logging.warning("LLM pipeline not available. Using fallback quest.")
            return _get_fallback_quest(quest_giver_faction_id)
        
        messages = [{"role": "user", "content": prompt}]
        try:
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            outputs = app.llm_pipeline(
                messages, max_new_tokens=1024, do_sample=True, temperature=0.8
            )
            response_text = outputs[0]["generated_text"][-1]["content"]
            logging.info(f"""--- RAW QUEST RESPONSE ---
{response_text}
------------------------""")
            cleaned_json = response_text.strip().replace("```json", "").replace("```", "")
            quest_data = json.loads(cleaned_json)
        except Exception as e:
            logging.error(f"Error during local LLM generation for quests: {e}", exc_info=True)
            return _get_fallback_quest(quest_giver_faction_id)
        finally:
            os.environ.pop("TOKENIZERS_PARALLELISM", None)

    # --- Process the response (from either source) ---
    if not isinstance(quest_data, dict) or "error" in quest_data:
        details = quest_data.get('details', 'No details') if isinstance(quest_data, dict) else "Non-dict response"
        logging.error(f"Quest generation failed: {details}")
        return _get_fallback_quest(quest_giver_faction_id)

    try:
        # Check if the LLM provided a specific target.
        target_faction_id = quest_data.get("target_faction")

        # If not, try to select a hostile one.
        if not target_faction_id:
            current_factions = faction_data if faction_data is not None else app.data.factions.FACTION_DATA
            hostile_factions = [
                fid for fid, rel in current_factions[quest_giver_faction_id]["relationships"].items()
                if rel == "Hostile" and fid in current_factions
            ]
            if hostile_factions:
                target_faction_id = random.choice(hostile_factions)
            else:
                # It's okay to have no specific target for some quests (e.g., from neutral cities)
                target_faction_id = None
                logging.info(f"No hostile factions found for {quest_giver_faction_id}, quest will have no target faction.")

        return Quest(
            name=quest_data["name"],
            description=quest_data["description"],
            dialog=quest_data["dialog"],
            objectives=quest_data["objectives"],
            rewards=quest_data["rewards"],
            quest_giver_faction=quest_giver_faction_id,
            target_faction=target_faction_id,
        )
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing LLM output for quests: {e}")
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
