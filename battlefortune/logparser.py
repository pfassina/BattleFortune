import os
import yaml
from time import sleep


def confirm_log(path):
    '''
    Checks if Log finished loading.
    '''

    valid = False
    with open(path + 'log.txt') as file:
        i = 0
        while i < 1000:
            blurb = file.read()
            start = blurb.find('getbattlecountfromvcr')  # battle loaded
            if start == -1:
                i += 1
                continue
            if blurb[start:].find('WhatPD') != -1: # Player Won
                valid = True
                break
            elif blurb[start:].find('spreadpath') != -1: # Player Lost
                valid = True
                break
            i += 1

    file.close()

    return valid


def parse_nations(log):
    loc = log.find('getbattlecount:') + 15
    armies = log[loc:].split(',', 3)[1:3]
    if armies[0].find('def') == -1:
        attacker = int(armies[0].strip().split(' ')[1])
        defender = int(armies[1].strip().split(' ')[1])
    else:
        defender = int(armies[0].strip().split(' ')[1])
        attacker = int(armies[1].strip().split(' ')[1])

    nations = {
        'attacker': attacker,
        'defender': defender
    }

    return nations


def find_battle(log):
    start = log.find('getbattlecountfromvcr') + 21
    end = log.rfind('getfatherland')
    battle = log[start:end-1]
    blurb = battle.split('\n')[1:]

    return blurb


def parse_battle(turn, battle, attacker, defender):

    battlelog = []
    for i in range(len(battle)):
        battle[i] = battle[i].split('(')[0].strip()
        battle[i] = [battle[i].split(':')[0], battle[i].split(':')[1].strip()]

        if battle[i][0] == '0' or battle[i][0] == '2':
            phase = 'before'
        else:
            phase = 'after'

        if battle[i][0] == '0' or battle[i][0] == '1':
            army = attacker
        else:
            army = defender

        count = int(battle[i][1].split(' ', 2)[0])
        count += int(battle[i][1].split(' ', 2)[1])
        unit = battle[i][1].split(' ', 2)[2]

        result = {
            'Turn': turn,
            'Phase': phase,
            'Army': army,
            'Unit': unit,
            'Count': count
        }

        battlelog.append(result)

    return battlelog


def parse_winner(turn, log, attacker, defender):

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

    turn_score = {
        'Turn': turn,
        'Nation': winner
    }

    return turn_score


def remove_turn_files(path, turn):

    files = [f for f in os.listdir(path) if os.path.isfile(
        os.path.join(path, f)) and f.startswith(str(turn) + '_')]
    for item in files:
        os.remove(os.path.join(path, item))


def parselog(turn):
    '''
    Parses Turn Log and returns two dictionary.
    First contains the winner nation, and the second the battle casualities.
    '''

    # get battle log
    stream = open('./battlefortune/data/config.yaml')
    path = yaml.load(stream)['gamepath'] + 'turns\\'
    log = open(path + str(turn) + '_log.txt', mode='r').read()

    print("^^^ log in parselog: " + log)

    # identify armies
    nations = parse_nations(log)
    attacker = nations['attacker']
    defender = nations['defender']

    # parse battle log
    battle = find_battle(log)
    battlelog = parse_battle(turn, battle, attacker, defender)
    # parse winner
    turn_score = parse_winner(turn, log, attacker, defender)

    # remove backup turn files
    remove_turn_files(path, turn)

    turn_log = {
        'nations': nations,
        'turn_score': turn_score,
        'battlelog': battlelog
    }

    return turn_log
