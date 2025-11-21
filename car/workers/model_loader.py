import logging
import os
from functools import partial
from typing import Any

# Updated to Gemma 2 (Unsloth variant for easier access)
MODEL_ID = "unsloth/gemma-2-2b-it"
LOCAL_MODEL_DIR = "models/unsloth-gemma-2-2b-it"

def load_pipeline() -> Any:
    """
    A simple synchronous function that performs the blocking I/O to load
    the transformers pipeline. This is designed to be run in a thread.
    """
    logging.info("Executing blocking pipeline load.")
    try:
        from transformers import pipeline
        import torch

        # Check if we have a local copy first
        model_path = MODEL_ID
        if os.path.exists(LOCAL_MODEL_DIR):
            logging.info(f"Found local model at {LOCAL_MODEL_DIR}, using it.")
            model_path = LOCAL_MODEL_DIR
        else:
            logging.warning(f"Local model not found at {LOCAL_MODEL_DIR}. Downloading/using cache from Hub.")

        # This is a blocking call. The transformers library handles caching on disk.
        pipeline_callable = partial(
            pipeline,
            "text-generation",
            model=model_path,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        llm_pipeline = pipeline_callable()
        logging.info("Blocking pipeline load complete.")
        return llm_pipeline
    except Exception as e:
        logging.error(f"Failed to load pipeline in worker: {e}", exc_info=True)
        return None
