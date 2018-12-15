import os
import yaml


def parselog(turn):
    '''
    Parses Turn Log and returns two dictionary.
    First contains the winner nation, and the second the battle casualities.
    '''

    # get battle log
    stream = open('./battlefortune/data/config.yaml')
    path = yaml.load(stream)['gamepath'] + 'turns\\'
    log = open(path + str(turn) + '_log.txt', mode='r').read()

    # identify armies
    loc = log.find('getbattlecount:') + 15
    armies = log[loc:].split(',', 3)[1:3]
    if armies[0].find('def') == -1:
        attacker = int(armies[0].strip().split(' ')[1])
        defender = int(armies[1].strip().split(' ')[1])
    else:
        defender = int(armies[0].strip().split(' ')[1])
        attacker = int(armies[1].strip().split(' ')[1])

    # parse battle log
    start = log.find('getbattlecountfromvcr') + 21
    end = log.find('SetMainEventMode')
    battle = log[start:end-1]
    blurb = battle.split('\n')[1:]

    # parse battle log
    battlelog = []
    for i in range(len(blurb)):
        blurb[i] = blurb[i].split('(')[0].strip()
        blurb[i] = [blurb[i].split(':')[0], blurb[i].split(':')[1].strip()]

        if blurb[i][0] == '0' or blurb[i][0] == '2':
            phase = 'before'
        else:
            phase = 'after'

        if blurb[i][0] == '0' or blurb[i][0] == '1':
            army = attacker
        else:
            army = defender

        count = int(blurb[i][1].split(' ', 2)[0])
        count += int(blurb[i][1].split(' ', 2)[1])
        unit = blurb[i][1].split(' ', 2)[2]

        result = {
            'Turn': turn,
            'Phase': phase,
            'Army': army,
            'Unit': unit,
            'Count': count
        }

        battlelog.append(result)

    # get winner
    p_loc = log.find('got turn info for player') + 25
    player = int(log[p_loc:].split('\n')[0])
    pwin = log.find('whatPD')

    if pwin > 0 and player == attacker:
        winner = attacker
    elif pwin > 0 and player == defender:
        winner = defender
    elif pwin == -1 and player == attacker:
        winner = defender
    elif pwin == -1 and player == defender:
        winner = attacker

    turnwinner = {
        'Turn': turn,
        'Nation': winner
    }

    # remove backup turn files
    files = [f for f in os.listdir(path) if os.path.isfile(
        os.path.join(path, f)) and f.startswith(str(turn) + '_')]
    for item in files:
        os.remove(os.path.join(path, item))

    return turnwinner, battlelog
