from batchrunner import main
from calc import battlecalc, wincalc


def run(turns):

    results = main(turns)
    winlog = results['winners']
    battlelog = results['battles']

    return {'winlog': winlog, 'battlelog': battlelog}


def calculate(winlog, battlelog):
    wincount = wincalc(winlog)
    battlecount = battlecalc(battlelog)

    return {'wincount': wincount, 'battlecount': battlecount}


def main(turns):

    logs = run(turns)
    results = calculate(logs['winlog'], logs['battlelog'])

    win_table = results['wincount']
    battle_table = results['battlecount']

    return {'win_table': win_table, 'battle_table': battle_table}
