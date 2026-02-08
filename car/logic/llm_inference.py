"""
Unified LLM inference interface.
Routes generation requests to either the local llama.cpp model
or the Gemini CLI, depending on app.generation_mode.
"""

import json
import logging
import threading

from .gemini_cli import generate_with_cli

_inference_lock = threading.Lock()


def _prepare_prompt_for_local(prompt: str) -> str:
    """Add model-specific instructions for Qwen3 to disable thinking mode."""
    return prompt + "\n/no_think"


def generate_json(app, prompt: str, json_schema: dict = None,
                  max_tokens: int = 1024, temperature: float = 0.8) -> dict | None:
    """
    Generate a JSON response from the LLM.

    Routes to gemini_cli or local llama.cpp based on app.generation_mode.
    When json_schema is provided and using local mode, grammar-constrained
    generation ensures the output is valid JSON matching the schema.

    Returns parsed dict on success, None on failure.
    """
    if app.generation_mode == "gemini_cli":
        return _generate_cli_json(app, prompt)

    return _generate_local_json(app, prompt, json_schema, max_tokens, temperature)


def generate_text(app, prompt: str, max_tokens: int = 512,
                  temperature: float = 0.8) -> str | None:
    """
    Generate a plain-text response from the LLM.

    Routes to gemini_cli or local llama.cpp based on app.generation_mode.
    Returns string on success, None on failure.
    """
    if app.generation_mode == "gemini_cli":
        return _generate_cli_text(app, prompt)

    return _generate_local_text(app, prompt, max_tokens, temperature)


def _generate_cli_json(app, prompt: str) -> dict | None:
    """Generate JSON via the configured CLI LLM tool."""
    response = generate_with_cli(
        prompt, parse_json=True,
        cli_preset=getattr(app, 'cli_preset', 'gemini'),
        custom_command=getattr(app, 'custom_cli_command', None) or None,
        custom_args=getattr(app, 'custom_cli_args', None) or None,
    )
    if isinstance(response, dict) and "error" not in response:
        return response
    if isinstance(response, dict):
        logging.error(f"CLI LLM returned error: {response.get('details', response)}")
    return None


def _generate_cli_text(app, prompt: str) -> str | None:
    """Generate plain text via the configured CLI LLM tool."""
    response = generate_with_cli(
        prompt, parse_json=False,
        cli_preset=getattr(app, 'cli_preset', 'gemini'),
        custom_command=getattr(app, 'custom_cli_command', None) or None,
        custom_args=getattr(app, 'custom_cli_args', None) or None,
    )
    if isinstance(response, str):
        return response
    if isinstance(response, dict) and "error" in response:
        logging.error(f"CLI LLM returned error: {response.get('details', response)}")
    return None


def _generate_local_json(app, prompt: str, json_schema: dict | None,
                         max_tokens: int, temperature: float) -> dict | None:
    """Generate JSON via local llama.cpp model with optional schema constraint."""
    if app.llm_pipeline is None:
        logging.warning("Local LLM pipeline not loaded. Cannot generate.")
        return None

    local_prompt = _prepare_prompt_for_local(prompt)
    messages = [{"role": "user", "content": local_prompt}]

    # Build response_format for grammar-constrained generation
    response_format = None
    if json_schema:
        response_format = {
            "type": "json_object",
            "schema": json_schema
        }

    with _inference_lock:
        try:
            response = app.llm_pipeline.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                response_format=response_format,
            )
            text = response["choices"][0]["message"]["content"]
            logging.info(f"--- RAW LOCAL LLM RESPONSE ---\n{text}\n-----------------------------")

            # Clean any markdown fencing the model might still produce
            cleaned = text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.replace("```json", "").replace("```", "").strip()

            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON from local LLM: {e}")
            return None
        except Exception as e:
            logging.error(f"Local LLM inference error: {e}", exc_info=True)
            return None


def _generate_local_text(app, prompt: str, max_tokens: int,
                         temperature: float) -> str | None:
    """Generate plain text via local llama.cpp model."""
    if app.llm_pipeline is None:
        logging.warning("Local LLM pipeline not loaded. Cannot generate.")
        return None

    local_prompt = _prepare_prompt_for_local(prompt)
    messages = [{"role": "user", "content": local_prompt}]

    with _inference_lock:
        try:
            response = app.llm_pipeline.create_chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = response["choices"][0]["message"]["content"]
            logging.info(f"--- RAW LOCAL LLM RESPONSE ---\n{text}\n-----------------------------")
            return text.strip()
        except Exception as e:
            logging.error(f"Local LLM inference error: {e}", exc_info=True)
            return None
