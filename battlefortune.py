from batchrunner import batchrun
from logcalc import battlecalc, wincalc


def BattleFortune(turns, game, nation):
    '''
    Runs BattleFortune program.
    Takes as input the number of turns to be simulated.
    Outputs simulation results.
    '''

    logs = batchrun(turns, game, nation)
    winners = wincalc(logs['winners'])
    battles = battlecalc(logs['battles'])

    output = {
        'win_table': winners,
        'battle_table': battles
    }

    return output
