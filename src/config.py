import logging
import os
import shutil
from dataclasses import dataclass, field
from typing import Optional, Self

import yaml


@dataclass
class ConfigData:
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


@dataclass
class Configuration:
    _config_data: Optional[ConfigData] = field(default=None)
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        _, _ = args, kwargs
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __post_init__(self) -> None:
        config_path = os.path.join("data", "config.yaml")
        if not os.path.exists(config_path):
            generate_config_file(config_path)
        self.update_data()

    @property
    def data(self) -> ConfigData:
        assert self._config_data
        return self._config_data

    def update_data(self) -> None:
        config_path = os.path.join("data", "config.yaml")
        if not os.path.exists(config_path):
            raise FileNotFoundError
        with open(config_path, "r") as file:
            config_dict = yaml.safe_load(file)
            self._config_data = ConfigData(**config_dict)

    def clone_game_files(self) -> None:
        logging.info("cloning game files")
        for turn in self.data.simulation_turns:
            if os.path.exists(self.data.simulation_path(turn)):
                logging.info("previous simulation files detected. removing old files.")
                shutil.rmtree(self.data.simulation_path(turn))
            logging.info(f"creating files for simulation {turn}")
            shutil.copytree(self.data.game_path, self.data.simulation_path(turn))

    def remove_cloned_files(self) -> None:
        for turn in self.data.simulation_turns:
            shutil.rmtree(self.data.simulation_path(turn))

    def move_log(self, turn: int, save_log: bool = False) -> None:
        src = os.path.join(self.data.dominions_path, "log.txt")
        dst = os.path.join(self.data.simulation_path(turn), "log.txt")
        shutil.copy(src, dst)

        if save_log:
            copy = os.path.join("logs", f"{self.data.game_name}_{turn}.log")
            shutil.copy(src, copy)


def generate_config_file(config_path: str) -> None:
    logging.info(f"creating new config file at {config_path}")
    config = {
        "dominions_path": None,
        "game_path": None,
        "game_name": None,
        "province": None,
        "simulations": None,
        "banner_x": 400,
        "banner_y": 310,
    }

    print(os.path.abspath(os.curdir))
    with open(config_path, "w") as file:
        yaml.dump(config, file)


CONFIG = Configuration()
