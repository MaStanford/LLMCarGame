import subprocess
import logging
import json
import shutil

def is_gemini_installed():
    """Checks if the Gemini CLI is installed and in the system's PATH."""
    return shutil.which("gemini") is not None

def generate_with_gemini_cli(prompt: str) -> dict:
    """
    Calls the Gemini CLI with the given prompt and returns the parsed JSON output.
    """
    if not is_gemini_installed():
        logging.error("Gemini CLI not found. Please install it to use this feature.")
        # Return a specific error structure that the caller can handle
        return {"error": "Gemini CLI not found."}

    command = ["gemini", "--yolo", "-p", prompt]
    
    try:
        logging.info("Calling Gemini CLI...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # The output from --yolo is the raw response, which should be our JSON
        raw_output = result.stdout
        logging.info(f"--- RAW GEMINI CLI RESPONSE ---\n{raw_output}\n-----------------------------")
        
        # Clean the response just in case
        cleaned_json = raw_output.strip().replace("```json", "").replace("```", "")
        
        return json.loads(cleaned_json)

    except subprocess.CalledProcessError as e:
        logging.error(f"Gemini CLI call failed with exit code {e.returncode}.")
        logging.error(f"Stderr: {e.stderr}")
        return {"error": "Gemini CLI call failed.", "details": e.stderr}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON from Gemini CLI output: {e}")
        return {"error": "Failed to parse JSON from Gemini CLI.", "details": str(e)}
    except Exception as e:
        logging.error(f"An unexpected error occurred with Gemini CLI: {e}", exc_info=True)
        return {"error": "An unexpected error occurred.", "details": str(e)}