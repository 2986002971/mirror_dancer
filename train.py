import os
import sys
from pathlib import Path

# Add project root to Python path to handle Hydra's directory changes
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

os.environ["MUJOCO_GL"] = "egl"
os.environ["LAZY_LEGACY_OP"] = "0"

# 直接解决 XML 解析冲突：强制设置正确的库路径
project_root = Path(__file__).resolve().parent
pixi_lib_path = str(project_root / ".pixi/envs/default/lib")
current_ld_path = os.environ.get("LD_LIBRARY_PATH", "")
if pixi_lib_path not in current_ld_path:
    os.environ["LD_LIBRARY_PATH"] = f"{pixi_lib_path}:{current_ld_path}"

import warnings

warnings.filterwarnings("ignore")
import hydra
import torch
from termcolor import colored

from common.buffer import Buffer
from common.logger import Logger
from common.offline_dataset import IRLBuffer
from common.parser import parse_cfg
from common.seed import set_seed
from envs import make_env
from tdmpc2 import TDMPC2
from trainer.online_trainer import OnlineTrainer

torch.backends.cudnn.benchmark = True


@hydra.main(config_name="config", config_path=".")
def train(cfg: dict):
    """
    Script for training single-task / multi-task TD-MPC2 agents.

    Most relevant args:
            `task`: task name (or mt30/mt80 for multi-task training)
            `model_size`: model size, must be one of `[1, 5, 19, 48, 317]` (default: 5)
            `steps`: number of training/environment steps (default: 10M)
            `seed`: random seed (default: 1)

    See config.yaml for a full list of args.

    Example usage:
    ```
            $ python train.py task=mt80 model_size=48
            $ python train.py task=mt30 model_size=317
            $ python train.py task=dog-run steps=7000000
    ```
    """
    assert torch.cuda.is_available()
    # wandb.login()
    # wandb.init(
    # 	project="tdmpc2-iqlearn-cube"
    # )
    assert cfg.steps > 0, "Must train for at least 1 step."
    cfg = parse_cfg(cfg)
    set_seed(cfg.seed)
    print(colored("Work dir:", "yellow", attrs=["bold"]), cfg.work_dir)

    trainer_cls = OnlineTrainer
    trainer = trainer_cls(
        cfg=cfg,
        env=make_env(cfg, test=True),
        agent=TDMPC2(cfg),
        buffer=Buffer(cfg),
        expert_buffer=IRLBuffer(cfg),
        logger=Logger(cfg),
    )
    # pdb.set_trace()
    # trainer = trainer_cls(
    # 	cfg=cfg,
    # 	env=gym.make(cfg.dataset),
    # 	agent=TDMPC2(cfg),
    # 	buffer=Buffer(cfg),
    # 	expert_buffer=IRLBuffer(cfg),
    # 	logger=Logger(cfg),
    # )
    trainer.train()
    print("\nTraining completed successfully")


if __name__ == "__main__":
    train()
