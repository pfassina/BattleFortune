import logging
import os
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


def generate_config_file(config_path: str) -> None:
    logging.info(f"creating new config file at {config_path}")
    config = {
        "dominions_path": "",
        "game_dir": "",
        "game_name": "",
        "province": "",
        "simulations": "",
        "banner_x": 400,
        "banner_y": 310,
    }

    with open(config_path, "w") as file:
        yaml.dump(config, file)


CONFIG: Configuration = Configuration()
