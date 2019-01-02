from batchrunner import batchrun
import os
from visualization import visualize
import yaml
import json


def setup(dom_path, game_path, max_threads, temp_path):
    """
    Setups config.yaml file with file paths.
    :param temp_path: OS path to dominions temporary files
    :param dom_path: OS path to dominions executable file
    :param game_path: OS path to game folder
    :param max_threads: maximum number of simultaneous threads
    :return: True when config file is updated
    """

    config = {
        'dompath': dom_path,
        'gamepath': game_path,
        'maxthreads': max_threads,
        'temppath': temp_path
    }

    stream = open('./battlefortune/data/config.yaml', 'w')
    yaml.dump(data=config, stream=stream)

    return True


def BattleFortune(turns, max_threads, game, province, dom_path, game_path, temp_path, dump_log=False):
    """
    Runs BattleFortune, simulate battles, and return results.
    :param temp_path: OS path to dominions temporary files
    :param turns: Number of Turns to be simulated.
    :param max_threads: Maximum number of simultaneous threads.
    :param game: Game to be simulated.
    :param province: Province where battle occurs.
    :param dom_path: dominions OS path.
    :param game_path: game OS path.
    :param dump_log: If true, created log files.
    :return: True when simulation is completed.
    """

    setup(dom_path=dom_path, game_path=game_path, max_threads=max_threads, temp_path=temp_path)

    logs = batchrun(turns, game, province)
    n = logs['nations']
    w = logs['winners']
    b = logs['battles']

    if dump_log:

        logpath = './battlefortune/logs/' + game + '/'
        if not os.path.exists(logpath):
            os.makedirs(logpath)

        yaml.dump(data=w, stream=open(logpath + 'winlog.yaml', 'w'))
        yaml.dump(data=b, stream=open(logpath + 'battlelog.yaml', 'w'))
        
        with open(logpath + 'battlelog.json', 'w') as outfile:  
            json.dump(b, outfile)

        with open(logpath + 'winlog.json', 'w') as outfile:
            json.dump(w, outfile)

    visualize(nations=n, win_log=w, battle_log=b, rounds=turns)

    return True
