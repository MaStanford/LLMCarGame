import subprocess
import logging
import json
import shutil

def is_gemini_installed():
    """Checks if the Gemini CLI is installed and in the system's PATH."""
    return shutil.which("gemini") is not None

def check_gemini_auth() -> bool:
    """
    Checks if the Gemini CLI is authenticated by running a simple command.
    Returns True if authenticated, False otherwise.
    """
    if not is_gemini_installed():
        return False
    
    try:
        # 'gemini models list' is a quick read-only command that requires auth
        subprocess.run(
            ["gemini", "models", "list"], 
            capture_output=True, 
            check=True,
            timeout=10 # Don't hang forever
        )
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False

def generate_with_gemini_cli(prompt: str, parse_json: bool = True) -> dict:
    """
    Calls the Gemini CLI with the given prompt.
    If parse_json is True, returns the parsed JSON output.
    Otherwise, returns the raw string output.
    """
    if not is_gemini_installed():
        logging.error("Gemini CLI not found. Please install it to use this feature.")
        return {"error": "Gemini CLI not found."}

    command = ["gemini", "--yolo", "-p", prompt]
    
    try:
        logging.info("Calling Gemini CLI...")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        raw_output = result.stdout
        logging.info(f"--- RAW GEMINI CLI RESPONSE ---\n{raw_output}\n-----------------------------")
        
        if not parse_json:
            return raw_output

        cleaned_json = raw_output.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_json)

    except subprocess.CalledProcessError as e:
        logging.error(f"Gemini CLI call failed with exit code {e.returncode}.")
        logging.error(f"Stderr: {e.stderr}")
        return {"error": "Gemini CLI call failed.", "details": e.stderr}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON from Gemini CLI output: {e}")
        # If JSON parsing fails, it might be a plain string response.
        # We return the raw output in this case, as it might be what the caller wants.
        return raw_output
    except Exception as e:
        logging.error(f"An unexpected error occurred with Gemini CLI: {e}", exc_info=True)
        return {"error": "An unexpected error occurred.", "details": str(e)}
