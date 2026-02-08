import logging
import os
from typing import Any

MODELS = {
    "small": {
        "repo": "Qwen/Qwen3-4B-GGUF",
        "filename": "qwen3-4b-q4_k_m.gguf",
        "local_path": "models/qwen3-4b-q4_k_m.gguf",
    },
    "large": {
        "repo": "Qwen/Qwen3-8B-GGUF",
        "filename": "qwen3-8b-q4_k_m.gguf",
        "local_path": "models/qwen3-8b-q4_k_m.gguf",
    },
}


def load_pipeline(model_size: str = "small") -> Any:
    """
    Loads the llama.cpp model from a local GGUF file.
    Designed to be run in a thread via Textual worker.
    """
    logging.info(f"Loading llama.cpp model (size={model_size})...")
    try:
        from llama_cpp import Llama

        model_config = MODELS.get(model_size, MODELS["small"])
        model_path = model_config["local_path"]

        if not os.path.exists(model_path):
            logging.error(
                f"Model file not found at '{model_path}'. "
                f"Run 'python download_model.py {model_size}' to download it."
            )
            return None

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
