import os
import json
import logging
from typing import List, Dict
from .gemini_cli import generate_with_gemini_cli

def generate_themes_from_llm(app) -> List[Dict[str, str]]:
    """
    Generates a list of three distinct themes for the game, using either the local
    LLM pipeline or the Gemini CLI based on the current settings.
    """
    with open("prompts/theme_generation_prompt.txt", "r") as f:
        prompt = f.read()

    logging.info(f"--- BUILDING THEME PROMPT ---\n{prompt}\n---------------------------")

    if app.generation_mode == "gemini_cli":
        theme_data = generate_with_gemini_cli(prompt)
    else:
        # Local pipeline logic
        if app.llm_pipeline is None or app.llm_pipeline == "unavailable":
            logging.warning("LLM pipeline not available. Using fallback themes.")
            return _get_fallback_themes()
        
        messages = [{"role": "user", "content": prompt}]
        try:
            os.environ["TOKENIZERS_PARALLELISM"] = "false"
            outputs = app.llm_pipeline(
                messages,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.9,
            )
            response_text = outputs[0]["generated_text"][-1]["content"]
            logging.info(f"--- RAW THEME RESPONSE ---\n{response_text}\n--------------------------")
            cleaned_json = response_text.strip().replace("```json", "").replace("```", "")
            theme_data = json.loads(cleaned_json)
        except Exception as e:
            logging.error(f"Error during local LLM generation for themes: {e}", exc_info=True)
            return _get_fallback_themes()
        finally:
            os.environ.pop("TOKENIZERS_PARALLELISM", None)

    # --- Process the response (from either source) ---
    if not isinstance(theme_data, dict) or "error" in theme_data:
        details = theme_data.get('details', 'No details') if isinstance(theme_data, dict) else "Non-dict response"
        logging.error(f"Theme generation failed: {details}")
        return _get_fallback_themes()

    if "themes" in theme_data and isinstance(theme_data["themes"], list) and len(theme_data["themes"]) == 3:
        return theme_data["themes"]
    else:
        logging.error(f"LLM output for themes has incorrect structure: {theme_data}")
        return _get_fallback_themes()

def _get_fallback_themes() -> List[Dict[str, str]]:
    """Returns a hardcoded list of themes for testing or when the LLM is unavailable."""
    return [
        {
            "name": "Classic Wasteland",
            "description": "A sun-scorched desert world of rust, dust, and desperate battles for the last drops of gasoline."
        },
        {
            "name": "Cyberpunk Drifters",
            "description": "Neon-drenched cityscapes at night, where cybernetically enhanced drivers clash in high-tech, corporate-sponsored duels."
        },
        {
            "name": "Mutant Menace",
            "description": "A world twisted by radiation, where bizarre creatures roam and strange new powers are waiting to be discovered."
        }
    ]
