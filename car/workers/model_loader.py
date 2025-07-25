import logging
from functools import partial
from typing import Any

MODEL_ID = "google/gemma-2b-it"

def load_pipeline() -> Any:
    """
    A simple synchronous function that performs the blocking I/O to load
    the transformers pipeline. This is designed to be run in a thread.
    """
    logging.info("Executing blocking pipeline load.")
    try:
        from transformers import pipeline
        import torch

        # This is a blocking call. The transformers library handles caching on disk.
        pipeline_callable = partial(
            pipeline,
            "text-generation",
            model=MODEL_ID,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda" if torch.cuda.is_available() else "cpu",
        )
        llm_pipeline = pipeline_callable()
        logging.info("Blocking pipeline load complete.")
        return llm_pipeline
    except Exception as e:
        logging.error(f"Failed to load pipeline in worker: {e}", exc_info=True)
        return None
