from batchrunner import batchrun
import yaml
from visualization import load_battlelog, distribution_charts


def setup(dompath, gamepath):
    '''
    Setups config.yaml file with file pathsself.
    Takes as input the absolute path for Dominions Game and Turn Files
    '''

    config = {
        'dompath': dompath,
        'gamepath': gamepath
    }

    stream = open('./battlefortune/data/config.yaml', 'w')
    yaml.dump(data=config, stream=stream)

    return


def BattleFortune(turns, game, province, dompath, gamepath, dumplog=False):
    '''
    Runs BattleFortune.
    Takes as required inputs:
        1. Number of turns to be simulated.
        2. Name of the Game to be simulated.
        3. Number of the province where the battle is happening.
        4. Dominions 5 executable path.
        5. Dominions 5 game folder path.
    Outputs distribution charts.
    '''

    setup(dompath, gamepath)

    logs = batchrun(turns, game, province)
    n = logs['nations']
    w = logs['winners']
    b = logs['battles']

    if dumplog:
        logpath = './battlefortune/logs/'
        yaml.dump(data=w, stream=open(logpath + 'winlog.yaml', 'w'))
        yaml.dump(data=b, stream=open(logpath + 'battlelog.yaml', 'w'))

    # wl = logcalc.wincalc(w)

    d = load_battlelog(b, n)
    distribution_charts(d, n)
