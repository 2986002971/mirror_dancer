#!/bin/bash

# 设置正确的库路径以解决XML冲突
export LD_LIBRARY_PATH="$(pwd)/.pixi/envs/default/lib:$LD_LIBRARY_PATH"

# 运行训练脚本并传递参数
pixi run python train.py "$@"
