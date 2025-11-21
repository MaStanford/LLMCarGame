#!/bin/bash

echo "Installing base requirements..."
pip install -r requirements.txt

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing Linux-specific requirements..."
    pip install -r requirements-linux.txt
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing macOS-specific requirements..."
    pip install -r requirements-macos.txt
else
    echo "Unsupported OS: Please install dependencies manually."
    exit 1
fi

echo "Installation complete."
touch .installed

echo ""
read -p "Do you want to download the AI model now? (~2GB) [y/N] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading model..."
    python download_model.py
else
    echo "Skipping model download. You can run 'python download_model.py' later."
fi
