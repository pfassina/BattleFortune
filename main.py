from batchrunner import main
from calc import battlecalc, wincalc


def BattleFortune(turns):
    '''
    Runs BattleFortune program.
    Takes as input the number of turns to be simulated.
    Outputs simulation results.
    '''

    logs = main(turns)
    winners = wincalc(logs['winners'])
    battles = battlecalc(logs['battles'])

    output = {
        'win_table': winners,
        'battle_table': battles
    }

    return output
