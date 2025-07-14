#!/bin/bash

# This script provides a convenient way to run the Car RPG.
# It handles platform-specific details, such as the LD_PRELOAD issue on Linux.

if [ ! -f ".installed" ]; then
    echo "Dependencies not installed. Please run install.sh first."
    exit 1
fi

# Check for --dev flag and set the environment variable
if [ "$1" == "--dev" ]; then
    export TEXTUAL="dev"
    shift # Remove --dev from the arguments
fi

# Check the operating system
OS="`uname`"
case $OS in
  'Linux')
    # On Linux, we need to preload the system's C++ library to ensure
    # compatibility with the audio libraries.
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
    python3 -m car "$@"
    ;;
  'Darwin') 
    # macOS
    python3 -m car "$@"
    ;;
  'Windows_NT')
    # Windows
    python -m car %*
    ;;
  *)
    echo "Unsupported operating system: $OS"
    exit 1
    ;;
esac
