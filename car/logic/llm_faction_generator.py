import os
import os
import json
import logging
import time
from .prompt_builder import build_faction_prompt

def generate_factions_from_llm(pipeline):
    """
    Generates a new set of factions by calling the language model.
    """
    if pipeline is None or pipeline == "unavailable":
        logging.warning("LLM pipeline not available. Using fallback factions.")
        return _get_fallback_factions()

    logging.info("Building faction prompt...")
    start_time = time.time()
    prompt = build_faction_prompt()
    messages = [{"role": "user", "content": prompt}]
    prompt_time = time.time()
    logging.info(f"Faction prompt built in {prompt_time - start_time:.2f} seconds.")
    logging.info("Calling LLM for faction generation...")

    try:
        # Disable tokenizers parallelism to prevent hangs in threaded environments
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        
        outputs = pipeline(
            messages,
            max_new_tokens=2048,
            do_sample=True,
            temperature=0.8,
        )
        inference_time = time.time()
        logging.info(f"LLM inference complete in {inference_time - prompt_time:.2f} seconds.")
        
        response_text = outputs[0]["generated_text"][-1]["content"]
        
        # Clean the response
        cleaned_json = response_text.strip().replace("```json", "").replace("```", "")
        faction_data = json.loads(cleaned_json)
        
        parsing_time = time.time()
        logging.info(f"Faction response parsed in {parsing_time - inference_time:.2f} seconds.")
        return faction_data
        
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        logging.error(f"Error parsing LLM output for factions: {e}")
        return _get_fallback_factions()
    except Exception as e:
        logging.error(f"Error during LLM generation: {e}", exc_info=True)
        return _get_fallback_factions()
    finally:
        # Best practice to clean up the environment variable
        os.environ.pop("TOKENIZERS_PARALLELISM", None)

def _get_fallback_factions():
    """Returns a hardcoded fallback response for testing or when the LLM is unavailable."""
    return {
      "the_vultures": {
        "name": "The Vultures", "hub_city_coordinates": [-30, 30], "control": 50,
        "relationships": {"desert_rats": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Neutral", "the_junction": "Neutral"},
        "units": ["rust_bucket", "raider_buggy", "technical"],
        "faction_boss": {"name": "Scrap King Klaw", "vehicle": "war_rig", "hp_multiplier": 5.0, "damage_multiplier": 2.5}
      },
      "desert_rats": {
        "name": "Desert Rats", "hub_city_coordinates": [40, -20], "control": 50,
        "relationships": {"the_vultures": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Allied", "the_junction": "Neutral"},
        "units": ["motorcycle", "hotrod", "muscle_car"],
        "faction_boss": {"name": "Road Captain Fury", "vehicle": "sports_car", "hp_multiplier": 3.0, "damage_multiplier": 3.5}
      },
      "corporate_guard": {
        "name": "Corporate Guard", "hub_city_coordinates": [25, 50], "control": 50,
        "relationships": {"the_vultures": "Hostile", "desert_rats": "Hostile", "the_convoy": "Hostile", "the_junction": "Neutral"},
        "units": ["sedan", "armored_truck", "peacekeeper"],
        "faction_boss": {"name": "Commander Valerius", "vehicle": "hatchback", "hp_multiplier": 4.0, "damage_multiplier": 3.0}
      },
      "the_convoy": {
        "name": "The Convoy", "hub_city_coordinates": [-40, -35], "control": 50,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Allied", "corporate_guard": "Hostile", "the_junction": "Neutral"},
        "units": ["truck", "van", "panel_wagon"],
        "faction_boss": {"name": "The Quartermaster", "vehicle": "truck", "hp_multiplier": 6.0, "damage_multiplier": 2.0}
      },
      "the_junction": {
        "name": "The Junction", "hub_city_coordinates": [0, 0], "control": 100,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Neutral", "corporate_guard": "Neutral", "the_convoy": "Neutral"},
        "units": ["rusty_sedan", "guard_truck"],
        "faction_boss": None
      }
    }

def _get_fallback_factions():
    """Returns a hardcoded fallback response for testing or when the LLM is unavailable."""
    return {
      "the_vultures": {
        "name": "The Vultures", "hub_city_coordinates": [-30, 30], "control": 50,
        "relationships": {"desert_rats": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Neutral", "the_junction": "Neutral"},
        "units": ["rust_bucket", "raider_buggy", "technical"],
        "faction_boss": {"name": "Scrap King Klaw", "vehicle": "war_rig", "hp_multiplier": 5.0, "damage_multiplier": 2.5}
      },
      "desert_rats": {
        "name": "Desert Rats", "hub_city_coordinates": [40, -20], "control": 50,
        "relationships": {"the_vultures": "Hostile", "corporate_guard": "Hostile", "the_convoy": "Allied", "the_junction": "Neutral"},
        "units": ["motorcycle", "hotrod", "muscle_car"],
        "faction_boss": {"name": "Road Captain Fury", "vehicle": "sports_car", "hp_multiplier": 3.0, "damage_multiplier": 3.5}
      },
      "corporate_guard": {
        "name": "Corporate Guard", "hub_city_coordinates": [25, 50], "control": 50,
        "relationships": {"the_vultures": "Hostile", "desert_rats": "Hostile", "the_convoy": "Hostile", "the_junction": "Neutral"},
        "units": ["sedan", "armored_truck", "peacekeeper"],
        "faction_boss": {"name": "Commander Valerius", "vehicle": "hatchback", "hp_multiplier": 4.0, "damage_multiplier": 3.0}
      },
      "the_convoy": {
        "name": "The Convoy", "hub_city_coordinates": [-40, -35], "control": 50,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Allied", "corporate_guard": "Hostile", "the_junction": "Neutral"},
        "units": ["truck", "van", "panel_wagon"],
        "faction_boss": {"name": "The Quartermaster", "vehicle": "truck", "hp_multiplier": 6.0, "damage_multiplier": 2.0}
      },
      "the_junction": {
        "name": "The Junction", "hub_city_coordinates": [0, 0], "control": 100,
        "relationships": {"the_vultures": "Neutral", "desert_rats": "Neutral", "corporate_guard": "Neutral", "the_convoy": "Neutral"},
        "units": ["rusty_sedan", "guard_truck"],
        "faction_boss": None
      }
    }
