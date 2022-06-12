from dataclasses import dataclass
import os
import shutil


@dataclass
class SimConfig:
    dominions_path: str
    game_dir: str
    game_name: str
    province: int
    simulations: int

    @property
    def game_path(self) -> str:
        return os.path.join(self.game_dir, self.game_name)

    @property
    def simulation_turns(self) -> list[int]:
        return [t for t in range(1, self.simulations + 1)]

    def simulation_path(self, turn: int) -> str:
        return f'{self.game_path}_{turn}'

    def clone_game_files(self) -> None:
        for turn in self.simulation_turns:
            if os.path.exists(self.simulation_path(turn)):
                shutil.rmtree(self.simulation_path(turn))
            shutil.copytree(self.game_path, self.simulation_path(turn))

    def remove_cloned_files(self) -> None:
        for turn in self.simulation_turns:
            shutil.rmtree(self.simulation_path(turn))

    def move_log(self, turn) -> None:
        src = os.path.join(self.dominions_path, 'log.txt')
        dst = os.path.join(self.simulation_path(turn), 'log.txt')
        shutil.move(src, dst)
