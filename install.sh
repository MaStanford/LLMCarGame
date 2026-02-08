#!/bin/bash
set -e

echo "=== The Genesis Module — Installer ==="
echo ""

# --- Check for python3 ---
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 is not installed or not in PATH."
    echo ""
    case "$OSTYPE" in
        linux*)
            echo "  Debian/Ubuntu:  sudo apt install python3 python3-pip python3-venv"
            echo "  Fedora:         sudo dnf install python3 python3-pip"
            echo "  Arch:           sudo pacman -S python python-pip"
            ;;
        darwin*)
            echo "  macOS (Homebrew): brew install python3"
            echo "  macOS (Xcode):    xcode-select --install"
            ;;
    esac
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found python3 ($PYTHON_VERSION)"

# --- Check for pip ---
if ! python3 -m pip -V &> /dev/null; then
    echo "ERROR: pip is not available for python3."
    echo ""
    case "$OSTYPE" in
        linux*)
            echo "  Debian/Ubuntu:  sudo apt install python3-pip"
            echo "  Fedora:         sudo dnf install python3-pip"
            echo "  Arch:           sudo pacman -S python-pip"
            ;;
        darwin*)
            echo "  macOS: python3 -m ensurepip --upgrade"
            ;;
    esac
    exit 1
fi

echo "Found pip ($(python3 -m pip -V | head -c 40)...)"
echo ""

# --- Create virtual environment ---
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv || {
        echo ""
        echo "ERROR: Failed to create virtual environment."
        case "$OSTYPE" in
            linux*)
                echo "  Debian/Ubuntu: sudo apt install python3-venv"
                ;;
        esac
        exit 1
    }
fi
echo "Virtual environment ready."

# Activate venv
source venv/bin/activate

# --- Install base requirements ---
echo ""
echo "Installing base requirements..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# --- Platform-specific: llama-cpp-python with GPU acceleration ---
echo ""
case "$OSTYPE" in
    darwin*)
        echo "Detected macOS — building llama-cpp-python with Metal (GPU) support..."
        CMAKE_ARGS="-DGGML_METAL=on" python3 -m pip install llama-cpp-python --force-reinstall --no-cache-dir
        ;;
    linux*)
        # Check for NVIDIA GPU
        if command -v nvidia-smi &> /dev/null; then
            echo "Detected NVIDIA GPU — building llama-cpp-python with CUDA support..."
            echo "  (This requires the CUDA toolkit. If it fails, install with: sudo apt install nvidia-cuda-toolkit)"
            CMAKE_ARGS="-DGGML_CUDA=on" python3 -m pip install llama-cpp-python --force-reinstall --no-cache-dir || {
                echo ""
                echo "WARNING: CUDA build failed. Falling back to CPU-only build."
                echo "  For GPU support, install the CUDA toolkit and try again."
                python3 -m pip install llama-cpp-python --force-reinstall --no-cache-dir
            }
        else
            echo "No NVIDIA GPU detected — installing llama-cpp-python (CPU only)."
            python3 -m pip install llama-cpp-python --force-reinstall --no-cache-dir
        fi

        # Install platform-specific extras if the file is non-empty
        if [ -s "requirements-linux.txt" ]; then
            python3 -m pip install -r requirements-linux.txt
        fi
        ;;
    *)
        echo "Installing llama-cpp-python (CPU only)..."
        python3 -m pip install llama-cpp-python --force-reinstall --no-cache-dir
        ;;
esac

# Install macOS extras if the file is non-empty
if [[ "$OSTYPE" == "darwin"* ]] && [ -s "requirements-macos.txt" ]; then
    python3 -m pip install -r requirements-macos.txt
fi

echo ""
echo "Installation complete."
touch .installed

# --- Offer model download ---
echo ""
read -p "Do you want to download an AI model now? (Required for local mode) [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 download_model.py
else
    echo "Skipping model download. Run 'python3 download_model.py' later to download."
fi

echo ""
echo "=== Setup complete! ==="
echo "Run the game with: ./run_game.sh"
