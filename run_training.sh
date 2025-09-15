#!/bin/bash

# --- Mirror Dancer Training Script ---
# This script automates the setup and execution of the training process.
# It ensures all dependencies are installed and environment variables are correctly set.

# 1. Check for Pixi
# Check if pixi is installed. If not, provide installation instructions.
if ! command -v pixi &> /dev/null
then
    echo "Error: pixi is not installed."
    echo "Please install pixi by following the instructions at https://pixi.sh/latest/"
    exit 1
fi

# 2. Install Dependencies
# Use pixi to install the project dependencies defined in pixi.toml.
echo "Ensuring all dependencies are installed with 'pixi install'..."
pixi install
if [ $? -ne 0 ]; then
    echo "Error: 'pixi install' failed. Please check your pixi.toml and environment."
    exit 1
fi

# 3. Set Environment for Headless Rendering
# Set the library path to include pixi's environment libraries.
# This is crucial for avoiding shared library conflicts (e.g., XML parser) and
# ensuring MuJoCo can find the correct rendering backends.
export LD_LIBRARY_PATH="$(pwd)/.pixi/envs/default/lib:$LD_LIBRARY_PATH"

# 4. Run Training
# Execute the main training script, passing along any command-line arguments.
echo "Starting the training process..."
pixi run python train.py "$@"

echo "Training script finished."