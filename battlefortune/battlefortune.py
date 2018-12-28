from batchrunner import batchrun
import os
from visualization import visualize
import yaml
import json


def setup(dompath, gamepath, maxthreads):
    """
    Setups config.yaml file with file paths.
    :param dompath: OS path to dominions executable file
    :param gamepath: OS path to game folder
    :param maxthreads: maximum number of simultaneous threads
    :return: True when config file is updated
    """

    config = {
        'dompath': dompath,
        'gamepath': gamepath,
        'maxthreads': maxthreads
    }

    stream = open('./battlefortune/data/config.yaml', 'w')
    yaml.dump(data=config, stream=stream)

    return True


def BattleFortune(turns, maxthreads, game, province, dompath, gamepath, dumplog=False):
    """
    Runs BattleFortune, simulate battles, and return results.
    :param turns: Number of Turns to be simulated.
    :param maxthreads: Maximum number of simultaneous threads.
    :param game: Game to be simulated.
    :param province: Province where battle occurs.
    :param dompath: dominions OS path.
    :param gamepath: game OS path.
    :param dumplog: If true, created log files.
    :return: True when simulation is completed.
    """

    setup(dompath, gamepath, maxthreads)

    logs = batchrun(turns, game, province)
    n = logs['nations']
    w = logs['winners']
    b = logs['battles']

    if dumplog:

        logpath = './battlefortune/logs/' + game + '/'
        if not os.path.exists(logpath):
            os.makedirs(logpath)

        yaml.dump(data=w, stream=open(logpath + 'winlog.yaml', 'w'))
        yaml.dump(data=b, stream=open(logpath + 'battlelog.yaml', 'w'))
        
        with open(logpath + 'battlelog.json', 'w') as outfile:  
            json.dump(b, outfile)

        with open(logpath + 'winlog.json', 'w') as outfile:
            json.dump(w, outfile)

    visualize(n, w, b)

    return True
