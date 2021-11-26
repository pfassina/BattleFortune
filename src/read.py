import os
import time

import yaml

from src import globals


def validate_log():
    """
    Checks if Log finished loading.
    :return: True if log is valid
    """

    valid = False

    i = 0
    time.sleep(0.1)
    while i < 1000000:
        with open(os.path.join(globals.DOM_PATH, 'log.txt')) as file:
            blurb = file.read()
            start = blurb.rfind('getbattlecountfromvcr')  # battle loaded
        if start == -1:
            i += 1
            continue
        if blurb[start:].rfind('whatPD') != -1:  # Player Won
            valid = True
            break
        if blurb[start:].rfind('[eof]') != -1:  # Player Lost
            time.sleep(0.1)
            if blurb[start:].rfind('whatPD') == -1:
                valid = True
                break
        i += 1

    return valid


def parse_nations(log):
    """
    Parses Nations from Log.
    :param log: log file
    :return: Dictionary with Nations Ids
    """

    armies = log[log.find('getbattlecount:') + 15:].split(',', 3)[1:3]
    defender = False if armies[0].find('def') == -1 else True
    a, b = [int(a.strip().split(' ')[1]) for a in armies]

    return {
        'attacker': b if defender else a,
        'defender': a if defender else b
    }


def find_battle(log):
    """
    Find Battle log blurb
    :param log: log file
    :return: battle log blurb
    """

    start = log.find('getbattlecountfromvcr') + 21
    end = log.rfind('restoremonarrays')

    return log[start:end-1].split('\n')[1:]


def parse_battle_entry(simulation_round, attacker, defender, battle_entry):
    """
    parse battle entry from battle battle log
    :param simulation_round:  Simulation Round
    :param attacker: attacker nation id
    :param defender: defender nation id
    :param battle_entry: entry on battle log
    :return: dictionary with battle entry results
    """

    cleaned_blurb = battle_entry.split('(')[0].strip()
    army, unit = [i.strip() for i in cleaned_blurb.split(':')]

    return {
            'Turn': simulation_round,
            'Phase': 'before' if army in ['0', '2'] else 'after',
            'Army': attacker if army in ['0', '1'] else defender,
            'Unit': unit.split(' ', 2)[2],
            'Count': sum([int(i) for i in unit.split(' ', 2)[:2]])
    }


def parse_battle(simulation_round, log, attacker, defender):
    """
    Parses Battle Blurb
    :param simulation_round: Simulation Round
    :param log: log file
    :param attacker: attacker nation id
    :param defender: defender nation id
    :return: battle log
    """
    return [parse_battle_entry(simulation_round, attacker, defender, i) for i in find_battle(log)]


def parse_winner(simulation_round, log, attacker, defender):
    """
    parses round winner from log
    :param simulation_round: simulation round
    :param log: log file
    :param attacker: attacker nation id
    :param defender: defender nation id
    :return: dictionary with the nation that won the turn
    """

    # parse log to find player nation
    player = int(log[log.find('got turn info for player') + 25:].split('\n')[0])

    # Define Winner based on Province Defense at Battle Province
    if log.find('whatPD') > 0:  # Player can add PD
        winner = attacker if player == attacker else defender
    else:
        winner = defender if player == attacker else defender

    return {
        'Turn': simulation_round,
        'Nation': winner
    }


def parse_log(simulation_round):
    """
    Parses Turn Log and returns turn log dictionary.
    :param simulation_round: Simulation round.
    :return: dictionary with nations, win log and battle log.
    """

    # get battle log
    round_path = f'{globals.GAME_PATH}_{str(simulation_round)}/'
    with open(round_path + 'log.txt', mode='r') as file:
        log = file.read()

    # identify armies
    nations = parse_nations(log)
    attacker = nations['attacker']
    defender = nations['defender']

    return {
        'nations': nations,
        'turn_score': parse_winner(simulation_round, log, attacker, defender),
        'battle_log': parse_battle(simulation_round, log, attacker, defender)
    }


def dump_log():
    """
    dump log into file
    :return: True if successful
    """

    log_path = f'./logs/{globals.GAME_NAME}/'
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    for log in ['winners', 'battles', 'nations']:
        path = os.path.join(log_path, f'{log}.yaml')
        with open(path, 'w') as file:
            yaml.dump(data=globals.LOGS[log], stream=file)

    return True


def combine_logs():
    """
    batch reads logs from all simulations
    :return: log list
    """

    valid_logs = [parse_log(r) for r in globals.VALID_ROUNDS]
    battle_logs = [log['battle_log'] for log in valid_logs]
    print(1)
    globals.LOGS = {
        'nations': valid_logs[0]['nations'],
        'winners': [log['turn_score'] for log in valid_logs],
        'battles': [battle for turn in battle_logs for battle in turn]
    }

    dump_log()
