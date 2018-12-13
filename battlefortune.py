from batchrunner import batchrun
from logcalc import wincalc
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

    stream = open('./data/config.yaml', 'w')
    yaml.dump(data=config, stream=stream)

    return print('config.yaml updated')


def BattleFortune(turns, game, nation):
    '''
    Runs BattleFortune program.
    Takes as input the number of turns to be simulated.
    Outputs simulation results.
    '''

    logs = batchrun(turns, game, nation)
    wins = wincalc(logs['winners'])

    output = {
        'wins': wins,
    }

    return output
