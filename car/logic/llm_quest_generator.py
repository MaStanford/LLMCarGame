import json
import logging
import random
from .prompt_builder import build_quest_prompt
from ..data.quests import (
    Quest, KillBossObjective, KillCountObjective,
    SurvivalObjective, DeliverPackageObjective, DefendLocationObjective
)
from .llm_inference import generate_json
from .llm_schemas import QUEST_SCHEMA

OBJECTIVE_CLASS_MAP = {
    "KillBossObjective": KillBossObjective,
    "KillCountObjective": KillCountObjective,
    "SurvivalObjective": SurvivalObjective,
    "DeliverPackageObjective": DeliverPackageObjective,
    "DefendLocationObjective": DefendLocationObjective,
}

def _instantiate_objectives(raw_objectives):
    """Convert raw objective data (from LLM or fallback) into Objective instances.
    Accepts formats like: ["KillBossObjective", ["arg1"]] or {"type": "KillBossObjective", "args": ["arg1"]}
    """
    objectives = []
    for obj_data in raw_objectives:
        if isinstance(obj_data, list) and len(obj_data) == 2:
            class_name, args = obj_data
        elif isinstance(obj_data, dict):
            class_name = obj_data.get("type", obj_data.get("class"))
            args = obj_data.get("args", [])
        else:
            logging.warning(f"Unknown objective format: {obj_data}")
            continue

        obj_class = OBJECTIVE_CLASS_MAP.get(class_name)
        if obj_class:
            objectives.append(obj_class(*args))
        else:
            logging.warning(f"Unknown objective class: {class_name}")

    if not objectives:
        objectives.append(KillCountObjective(3))
    return objectives

def generate_quest_from_llm(game_state, quest_giver_faction_id, app, faction_data=None):
    """
    Generates a new quest by calling the language model.
    Can be passed faction_data directly to override the global data, useful for workers.
    """
    prompt = build_quest_prompt(game_state, quest_giver_faction_id, faction_data)

    quest_data = generate_json(app, prompt, json_schema=QUEST_SCHEMA, max_tokens=1024, temperature=0.8)

    if quest_data is None:
        return _get_fallback_quest(quest_giver_faction_id)

    # --- Process the response ---
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
            objectives=_instantiate_objectives(quest_data["objectives"]),
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
        objectives=_instantiate_objectives([["KillBossObjective", ["Scrap King Klaw"]]]),
        rewards={"xp": 500, "cash": 1000},
        quest_giver_faction=quest_giver_faction_id,
        target_faction="the_vultures",
    )
