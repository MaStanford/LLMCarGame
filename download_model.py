import os
from huggingface_hub import snapshot_download

# --- Configuration ---
MODEL_ID = "unsloth/gemma-2-2b-it"
MODEL_DIR = "models/unsloth-gemma-2-2b-it"
# -------------------

def download_model():
    """
    Downloads the specified model from the Hugging Face Hub using snapshot_download.
    This ensures all necessary files for Transformers are present.
    """
    print("--- Model Downloader ---")
    
    # Ensure the model directory exists
    if not os.path.exists(MODEL_DIR):
        print(f"Creating model directory: {MODEL_DIR}")
        os.makedirs(MODEL_DIR)

    print(f"Downloading '{MODEL_ID}' to '{MODEL_DIR}'...")
    print("This may take a while depending on your internet connection.")

    try:
        snapshot_download(
            repo_id=MODEL_ID,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False, # We want the actual files
            resume_download=True
        )
        print("\nDownload complete!")
        print(f"Model saved to: {MODEL_DIR}")
    except Exception as e:
        print(f"\nAn error occurred during download: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    download_model()
