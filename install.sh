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
