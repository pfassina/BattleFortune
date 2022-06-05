from dataclasses import dataclass
import os


@dataclass
class SimConfig:
    dominions_path: str
    game_dir: str
    game_name: str
    province: int
    simulations: int

    @property
    def game_path(self):
        return os.path.join(self.game_dir, self.game_name)