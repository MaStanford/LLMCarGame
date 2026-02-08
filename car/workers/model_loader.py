import logging
import os
import subprocess
import sys
from typing import Any

MODELS = {
    "small": {
        "repo": "Qwen/Qwen3-4B-GGUF",
        "filename": "Qwen3-4B-Q4_K_M.gguf",
        "local_path": "models/Qwen3-4B-Q4_K_M.gguf",
    },
    "large": {
        "repo": "Qwen/Qwen3-8B-GGUF",
        "filename": "Qwen3-8B-Q4_K_M.gguf",
        "local_path": "models/Qwen3-8B-Q4_K_M.gguf",
    },
}


def _preflight_check() -> bool:
    """
    Test llama.cpp in a subprocess to catch segfaults before they kill the game.
    Returns True if the library works, False if it crashes or is missing.
    """
    test_script = (
        "from llama_cpp.llama_cpp import llama_backend_init; "
        "llama_backend_init(); "
        "print('OK')"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", test_script],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and "OK" in result.stdout:
            return True
        logging.error(
            f"llama.cpp preflight failed (exit {result.returncode}). "
            f"stderr: {result.stderr.strip()}"
        )
        return False
    except subprocess.TimeoutExpired:
        logging.error("llama.cpp preflight timed out.")
        return False
    except Exception as e:
        logging.error(f"llama.cpp preflight error: {e}")
        return False


def load_pipeline(model_size: str = "small") -> Any:
    """
    Loads the llama.cpp model from a local GGUF file.
    Designed to be run in a thread via Textual worker.
    """
    logging.info(f"Loading llama.cpp model (size={model_size})...")

    # Check that llama-cpp-python is installed
    try:
        import llama_cpp  # noqa: F401
    except ImportError:
        logging.error(
            "llama-cpp-python is not installed. "
            "Run 'python3 -m pip install llama-cpp-python' to install it."
        )
        return None

    # Check model file exists
    model_config = MODELS.get(model_size, MODELS["small"])
    model_path = model_config["local_path"]

    if not os.path.exists(model_path):
        logging.error(
            f"Model file not found at '{model_path}'. "
            f"Run 'python3 download_model.py {model_size}' to download it."
        )
        return None

    # Preflight: test llama.cpp in a subprocess to catch segfaults
    if not _preflight_check():
        logging.error(
            "llama.cpp crashed during preflight check. "
            "The library may be incompatible with this system. "
            "Try reinstalling: python3 -m pip install llama-cpp-python --force-reinstall --no-cache-dir"
        )
        return None

    try:
        from llama_cpp import Llama

        llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Use all layers on GPU (Metal/CUDA); falls back to CPU gracefully
            n_ctx=4096,
            verbose=False,
        )
        logging.info(f"llama.cpp model loaded successfully from {model_path}")
        return llm
    except Exception as e:
        logging.error(f"Failed to load llama.cpp model: {e}", exc_info=True)
        return None
