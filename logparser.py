import os
from pathlib import Path

def parsewinner(turn):

    home = str(Path.home()) + '\\AppData\\Roaming\\Dominions5\\savedgames\\test\\turns\\'
    log = open(home + str(turn) + '_log.txt', mode='r').read()
    loc = log.find('the winner is ') + 14
    winner = int(log[loc:loc+10].split(' ')[0])

    # remove files
    files = [f for f in os.listdir(home) if os.path.isfile(os.path.join(home, f)) and f.startswith(str(turn) + '_')]
    for item in files:
        os.remove(os.path.join(home, item))

    return {'Turn': turn, 'Winner': winner}


def parsebattle(turn):

    # get battle log
    home = str(Path.home()) + '\\AppData\\Roaming\\Dominions5\\savedgames\\test\\turns\\'
    log = open(home + str(turn) + '_log.txt', mode='r').read()

    # identify armies
    loc = log.find('getbattlecount:') + 15
    armies = log[loc:].split(',', 3)[1:3]
    attacker = int(armies[0].strip().split(' ')[1])
    defender = int(armies[1].strip().split(' ')[1])

    # parse battle log

    home = str(Path.home()) + '\\AppData\\Roaming\\Dominions5\\savedgames\\test\\turns\\'
    log = open(home + str(turn) + '_log.txt', mode='r').read()

    loc = log.find('getbattlecountfromvcr') + 21
    battle = log[loc:len(log)-1]
    battleblurb = battle.split('\n')[1:]

    # parse battle log
    battlelog = []
    for i in range(len(battleblurb)):
        battleblurb[i] = battleblurb[i].split('(')[0].strip()
        battleblurb[i] = [battleblurb[i].split(':')[0], battleblurb[i].split(':')[1].strip()]

        if battleblurb[i][0] == '0' or battleblurb[i][0] == '2':
            phase = 'before'
        else:
            phase = 'after'

        if battleblurb[i][0] == '0' or battleblurb[i][0] == '1':
            army = attacker
        else:
            army = defender

        count = int(battleblurb[i][1].split(' ',2)[0]) + int(battleblurb[i][1].split(' ',2)[1])
        unit = battleblurb[i][1].split(' ',2)[2]


        battlelog.append({'Turn': turn, 'Phase': phase, 'Army': army, 'Count': count, 'Unit': unit})

    # remove files
    files = [f for f in os.listdir(home) if os.path.isfile(os.path.join(home, f)) and f.startswith(str(turn) + '_')]
    for item in files:
        os.remove(os.path.join(home, item))

    return battlelog
