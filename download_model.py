import os
import sys
from huggingface_hub import hf_hub_download

# --- Configuration ---
MODELS = {
    "small": {
        "repo": "Qwen/Qwen3-4B-GGUF",
        "filename": "qwen3-4b-q4_k_m.gguf",
        "description": "Qwen3 4B (Q4_K_M) — ~2.5 GB, fast, good for most hardware",
    },
    "large": {
        "repo": "Qwen/Qwen3-8B-GGUF",
        "filename": "qwen3-8b-q4_k_m.gguf",
        "description": "Qwen3 8B (Q4_K_M) — ~5 GB, higher quality, needs more RAM",
    },
}
MODEL_DIR = "models"
# -------------------


def download_model(size: str = None):
    """
    Downloads GGUF model files from Hugging Face Hub.
    Supports interactive selection or CLI argument.
    """
    if size is None:
        print("--- Model Downloader ---")
        print("Choose a model size:")
        print(f"  1. Small — {MODELS['small']['description']}")
        print(f"  2. Large — {MODELS['large']['description']}")
        print(f"  3. Both")
        choice = input("Enter choice [1/2/3]: ").strip()
        sizes = {"1": ["small"], "2": ["large"], "3": ["small", "large"]}
        selected = sizes.get(choice, ["small"])
    else:
        if size not in MODELS:
            print(f"Unknown model size '{size}'. Options: small, large")
            sys.exit(1)
        selected = [size]

    os.makedirs(MODEL_DIR, exist_ok=True)

    for s in selected:
        config = MODELS[s]
        dest = os.path.join(MODEL_DIR, config["filename"])

        if os.path.exists(dest):
            print(f"Already downloaded: {dest}")
            continue

        print(f"Downloading {config['filename']} from {config['repo']}...")
        print("This may take a while depending on your internet connection.")

        try:
            hf_hub_download(
                repo_id=config["repo"],
                filename=config["filename"],
                local_dir=MODEL_DIR,
                local_dir_use_symlinks=False,
                resume_download=True,
            )
            print(f"Downloaded to {dest}")
        except Exception as e:
            print(f"An error occurred during download: {e}")
            print("Please check your internet connection and try again.")

    print("\nDone.")


if __name__ == "__main__":
    size_arg = sys.argv[1] if len(sys.argv) > 1 else None
    download_model(size_arg)
