import os
from huggingface_hub import hf_hub_download

# --- Configuration ---
MODEL_ID = "google/gemma-2b-it"
MODEL_FILENAME = "gemma-2b-it.gguf"
MODEL_DIR = "models"
# -------------------

def download_model():
    """
    Downloads the specified GGUF model from the Hugging Face Hub if it doesn't already exist.
    """
    print("--- Model Downloader ---")
    
    # Ensure the model directory exists
    if not os.path.exists(MODEL_DIR):
        print(f"Creating model directory: {MODEL_DIR}")
        os.makedirs(MODEL_DIR)

    model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)

    if os.path.exists(model_path):
        print(f"Model already exists at: {model_path}")
        print("Skipping download.")
        return

    print(f"Model not found. Downloading '{MODEL_FILENAME}' from '{MODEL_ID}'...")
    print("This may take a while depending on your internet connection.")

    try:
        hf_hub_download(
            repo_id=MODEL_ID,
            filename=MODEL_FILENAME,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False, # We want the actual file
            resume_download=True
        )
        print("\nDownload complete!")
        print(f"Model saved to: {model_path}")
    except Exception as e:
        print(f"\nAn error occurred during download: {e}")
        print("Please check your internet connection and try again.")
        print(f"If the problem persists, you can try manually downloading the file from: https://huggingface.co/{MODEL_ID}/tree/main")

if __name__ == "__main__":
    download_model()
