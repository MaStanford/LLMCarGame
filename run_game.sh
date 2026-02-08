#!/bin/bash

# This script provides a convenient way to run The Genesis Module.
# It handles platform-specific details and virtual environment activation.

if [ ! -f ".installed" ]; then
    echo "Dependencies not installed. Please run install.sh first."
    exit 1
fi

# Activate virtual environment if present
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check for --dev flag and set the environment variable
if [ "$1" == "--dev" ]; then
    export TEXTUAL="dev"
    shift
fi

# Check for --log flag to enable file logging
LOG_FLAG=""
if [ "$1" == "--log" ]; then
    LOG_FLAG="--log"
    shift
fi

# Check the operating system
OS="$(uname)"
case $OS in
  'Linux')
    # On Linux, preload the system's C++ library for audio compatibility
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
    python3 -m car "$@"
    ;;
  'Darwin')
    python3 -m car "$@"
    ;;
  *)
    echo "Unsupported operating system: $OS"
    echo "Try running directly: python3 -m car"
    exit 1
    ;;
esac
