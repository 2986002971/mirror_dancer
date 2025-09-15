# Mirror Dancer

This project implements the Mirror-Dancer algorithm, a reinforcement learning agent.

## Dependencies

This project is designed to run on a Linux environment and has the following system-level dependencies:

1.  **Linux OS**: Ubuntu 20.04 or later is recommended.
2.  **NVIDIA GPU**: A CUDA-enabled GPU is required for training.
3.  **CUDA Toolkit**: Ensure you have a compatible NVIDIA driver and CUDA Toolkit installed.
4.  **EGL Libraries**: For headless rendering (required by the MuJoCo physics simulator), you need EGL. On Debian/Ubuntu, install it with:
    ```bash
    sudo apt-get update && sudo apt-get install -y libegl1-mesa-dev
    ```
5.  **Pixi**: This project uses `pixi` to manage Python dependencies and environments. Please install it by following the official instructions at [https://pixi.sh/latest/](https://pixi.sh/latest/).

## Setup and Running

The project includes a "one-click" script to handle setup and execution.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/2986002971/mirror_dancer.git
    cd mirror_dancer
    ```

2.  **Make the script executable:**
    ```bash
    chmod +x run_training.sh
    ```

3.  **Run the training:**
    ```bash
    ./run_training.sh task=hopper-hop
    ```

### How the Script Works

The `run_training.sh` script automates the following steps:
- It first checks if `pixi` is installed on your system.
- It runs `pixi install` to create the environment and install all Python packages defined in `pixi.toml`.
- It correctly sets the `LD_LIBRARY_PATH` environment variable. This is a crucial step to ensure the Python interpreter can find the shared libraries within the `pixi` environment, which is necessary for libraries like `dm_control` to function correctly.
- Finally, it executes the main `train.py` script, passing along any arguments you provide (e.g., `task=hopper-hop`).
