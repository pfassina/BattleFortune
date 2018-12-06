from batchrunner import batchrun
from logcalc import battlecalc, wincalc
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

    stream = open('config.yaml', 'w')
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
    battles = battlecalc(logs['battles'])

    output = {
        'wins': wins,
        'battles': battles
    }

    return output
