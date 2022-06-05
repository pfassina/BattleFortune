import os
import shutil

from src.config import SimConfig


def clone_game_files(game_path: str, simulations: int) -> None:
    """
    Clones game files for each round.
    :return: True when all files were cloned
    """

    for i in range(simulations):
        turn_path = f'{game_path}_{i + 1}'
        if os.path.exists(turn_path):
            shutil.rmtree(turn_path)
        shutil.copytree(game_path, turn_path)


def move_log(config: SimConfig, simulation_round: int) -> None:
    """
    Backups turn and log files.
    :param simulation_round: simulation round
    """

    src = os.path.join(f'{config.dominions_path}', 'log.txt')
    dst = os.path.join(f'{config.game_path}_{simulation_round}', 'log.txt')
    shutil.move(src, dst)


def remove_cloned_files(game_path: str, simulations: int) -> None:
    """
    Cleans up temporary folders
    :return: True when temporary turn files are removed.
    """

    for i in range(simulations):
        folder = f'{game_path}_{i + 1}'
        shutil.rmtree(folder)
