import os

import yaml
import json

import run
import prepare
import visualize


def setup(dom_path, game_path, temp_path):
    """
    Setups config.yaml file with file paths.
    :param temp_path: OS path to dominions temporary files
    :param dom_path: OS path to dominions executable file
    :param game_path: OS path to game folder
    :return: True when config file is updated
    """

    config = {
        'dom_path': dom_path,
        'game_path': game_path,
        'temp_path': temp_path
    }

    stream = open('./battlefortune/data/config.yaml', 'w')
    yaml.dump(data=config, stream=stream)

    return True


def battlefortune(rounds, game, province, dump_log=False):
    """
    Runs BattleFortune, simulate battles, and return results.
    :param rounds: Number of Turns to be simulated.
    :param game: Game to be simulated.
    :param province: Province where battle occurs.
    :param dump_log: If true, created log files.
    :return: True when simulation is completed.
    """

    # SETUP
    with open('./battlefortune/data/config.yaml') as config:
        paths = yaml.load(config)

    dp = paths['dom_path']
    gp = paths['game_path']
    tp = paths['temp_path']

    # PREPARE
    prepare.clone_game(path=gp, rounds=rounds)

    # RUN
    logs = run.simulation(dom_path=dp, game_path=gp, temp_path=tp, game=game, rounds=rounds, province=province)

    # COLLECT
    n = logs['nations']
    w = logs['winners']
    b = logs['battles']

    # DUMP
    if dump_log:

        log_path = './battlefortune/logs/' + game + '/'
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        yaml.dump(data=w, stream=open(log_path + 'winlog.yaml', 'w'))
        yaml.dump(data=b, stream=open(log_path + 'battlelog.yaml', 'w'))

        with open(log_path + 'battlelog.json', 'w') as outfile:
            json.dump(b, outfile)

        with open(log_path + 'winlog.json', 'w') as outfile:
            json.dump(w, outfile)

    # DISPLAY
    visualize.visualize(nations=n, win_log=w, battle_log=b, rounds=rounds)

    return True
