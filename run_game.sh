#!/bin/bash

# This script provides a convenient way to run the Car RPG.
# It handles platform-specific details, such as the LD_PRELOAD issue on Linux.

# Check the operating system
OS="`uname`"
case $OS in
  'Linux')
    # On Linux, we need to preload the system's C++ library to ensure
    # compatibility with the audio libraries.
    export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
    python3 -m car
    ;;
  'Darwin') 
    # macOS
    python3 -m car
    ;;
  'Windows_NT')
    # Windows
    python -m car
    ;;
  *)
    echo "Unsupported operating system: $OS"
    exit 1
    ;;
esac
