import os
import shutil
from dataclasses import dataclass

import yaml


@dataclass
class SimConfig:
    dominions_path: str
    game_dir: str
    game_name: str
    province: int
    simulations: int
    banner_x: int
    banner_y: int

    @property
    def game_path(self) -> str:
        return os.path.join(self.game_dir, self.game_name)

    @property
    def simulation_turns(self) -> list[int]:
        return [t for t in range(1, self.simulations + 1)]

    def simulation_path(self, turn: int) -> str:
        return f"{self.game_path}_{turn}"

    def clone_game_files(self) -> None:
        for turn in self.simulation_turns:
            if os.path.exists(self.simulation_path(turn)):
                shutil.rmtree(self.simulation_path(turn))
            shutil.copytree(self.game_path, self.simulation_path(turn))

    def remove_cloned_files(self) -> None:
        for turn in self.simulation_turns:
            shutil.rmtree(self.simulation_path(turn))

    def move_log(self, turn) -> None:
        src = os.path.join(self.dominions_path, "log.txt")
        dst = os.path.join(self.simulation_path(turn), "log.txt")
        shutil.move(src, dst)


def generate_config_file() -> None:
    if not os.path.exists("./logs"):
        os.mkdir("logs")
    if not os.path.exists("./img"):
        os.mkdir("img")
    if not os.path.exists("./csv"):
        os.mkdir("csv")

    if not os.path.exists("./data/config.yaml"):
        config = {
            "dominions_path": None,
            "game_path": None,
            "game_name": None,
            "province": None,
            "simulations": None,
            "banner_x": 400,
            "banner_y": 310,
        }

        with open("data/config.yaml", "w") as file:
            yaml.dump(config, file)
