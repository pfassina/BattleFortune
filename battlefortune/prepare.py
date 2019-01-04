import os
import shutil
import yaml


def clone_game(path, rounds):
    """
    Clones game files for each round.
    :param path: game folder
    :param rounds: total number of simulations
    :return: True when all files were cloned
    """

    for i in range(1, rounds + 1):
        turn_path = path[:-1] + str(i) + '/'
        if not os.path.exists(turn_path):
            shutil.copytree(path, turn_path)
        else:
            shutil.rmtree(turn_path)
            shutil.copytree(path, turn_path)

    return True


def move_log(dom_path, round_path):
    """
    Backups turn and log files.
    :param round_path: simulation round path
    :param dom_path: dominions path
    :return: True when files are backed-up
    """

    # Backlog Log file
    src = dom_path + 'log.txt'
    dst = round_path + 'log.txt'
    shutil.move(src, dst)

    return True


def clean_turns(rounds):
    """
    Cleans up temporary folders
    :param rounds: number of simulation rounds
    :return: True when temporary turn files are removed.
    """

    path = yaml.load(open('./battlefortune/data/config.yaml'))['game_path']

    for i in range(1, rounds + 1):
        folder = path[:-1] + str(i) + '/'
        shutil.rmtree(folder)

    return True


def delete_temp(path):
    """
    Delete Temporary Dominions files.
    :return: True when log is deleted.
    """

    temp_dir = os.listdir(path)
    temp = [f for f in temp_dir if f.startswith('dom5')]

    for item in temp:
        shutil.rmtree(path + item + '/')

    return True
