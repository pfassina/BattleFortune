import os
import shutil

from src import globals


def clone_game_files():
    """
    Clones game files for each round.
    :return: True when all files were cloned
    """

    for i in range(1, globals.SIMULATIONS + 1):
        turn_path = f'{globals.GAME_PATH}_{str(i)}/'
        if not os.path.exists(turn_path):
            shutil.copytree(globals.GAME_PATH, turn_path)
        else:
            shutil.rmtree(turn_path)
            shutil.copytree(globals.GAME_PATH, turn_path)


def move_log(simulation_round):
    """
    Backups turn and log files.
    :param simulation_round: simulation round
    """

    # Backlog Log file
    src = os.path.join(globals.DOM_PATH, 'log.txt')
    dst = os.path.join(f'{globals.GAME_PATH}_{str(simulation_round)}/', 'log.txt')
    shutil.move(src, dst)


def remove_cloned_files():
    """
    Cleans up temporary folders
    :return: True when temporary turn files are removed.
    """

    for i in range(1, globals.SIMULATIONS + 1):
        folder = f'{globals.GAME_PATH}_{str(i)}/'
        shutil.rmtree(folder)

    return True
