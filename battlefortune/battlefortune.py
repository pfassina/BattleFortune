from batchrunner import batchrun
import logcalc
import yaml


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


def BattleFortune(turns, game, dompath, gamepath, dumplog=False):
    '''
    Runs BattleFortune.
    Takes as input:
        1. Number of turns to be simulated.
        2. Game to be simulated.
        3. Dominions 5 executable path.
        4. Dominions 5 game path.
        5. Option to save logs to file.
    Outputs parsed simulation results.
    '''

    setup(dompath, gamepath)

    logs = batchrun(turns, game)
    w = logs['winners']
    b = logs['battles']

    if dumplog:
        logpath = './battlefortune/logs/'
        yaml.dump(data=w, stream=open(logpath + 'winlog.yaml', 'w'))
        yaml.dump(data=b, stream=open(logpath + 'battlelog.yaml', 'w'))

    wl = logcalc.wincalc(w)
    bl = logcalc.pivot_battlelog(b)

    output = {
        'wins': wl,
        'battles': bl,
    }

    return output
