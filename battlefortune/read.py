

def validate_log(path):
    """
    Checks if Log finished loading.
    :param path: log path
    :return: True if log is valid
    """

    valid = False

    i = 0
    while i < 1000000:
        with open(path + 'log.txt') as file:
            blurb = file.read()
        start = blurb.rfind('getbattlecountfromvcr')  # battle loaded
        if start == -1:
            i += 1
            continue
        if blurb[start:].rfind('whatPD') != -1:  # Player Won
            valid = True
            break
        if blurb[start:].rfind('createoverlaytex') != -1:  # Player Lost
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
    """
    Find Battle log blurb
    :param log: log file
    :return: battle log blurb
    """
    start = log.find('getbattlecountfromvcr') + 21
    end = log.rfind('getfatherland')
    battle = log[start:end-1]
    blurb = battle.split('\n')[1:]

    return blurb


def parse_battle(battle_round, battle, attacker, defender):
    """
    Parses Battle Blurb
    :param battle_round: Simulation Round
    :param battle: battle blurb
    :param attacker: attacker nation id
    :param defender: defender nation id
    :return: battle log
    """

    battle_log = []
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
            'Turn': battle_round,
            'Phase': phase,
            'Army': army,
            'Unit': unit,
            'Count': count
        }

        battle_log.append(result)

    return battle_log


def parse_winner(battle_round, log, attacker, defender):
    """
    parses round winner from log
    :param battle_round: simulation round
    :param log: log file
    :param attacker: attacker nation id
    :param defender: defender nation id
    :return: dictionary with the nation that won the turn
    """

    p_loc = log.find('got turn info for player') + 25
    player = int(log[p_loc:].split('\n')[0])
    pd_log_string = log.find('whatPD')

    # Define Winner based on Province Defense at Battle Province
    winner = None
    if pd_log_string > 0 and player == attacker:  # Player is attacker and won battle
        winner = attacker
    elif pd_log_string > 0 and player == defender:  # Player is defender and won battle
        winner = defender
    elif pd_log_string == -1 and player == attacker:  # Player is attacker lost battle
        winner = defender
    elif pd_log_string == -1 and player == defender:  # Player is defender and list battle
        winner = attacker

    turn_score = {
        'Turn': battle_round,
        'Nation': winner
    }

    return turn_score


def parse_log(game_path, battle_round):
    """
    Parses Turn Log and returns turn log dictionary.
    :param game_path:  game path
    :param battle_round: Simulation round.
    :return: dictionary with nations, win log and battle log.
    """

    # get battle log
    round_path = game_path[:-1] + str(battle_round) + '/'
    with open(round_path + 'log.txt', mode='r') as file:
        log = file.read()

    # identify armies
    nations = parse_nations(log)
    attacker = nations['attacker']
    defender = nations['defender']

    # parse battle log
    battle = find_battle(log)
    battle_log = parse_battle(battle_round, battle, attacker, defender)
    # parse winner
    turn_score = parse_winner(battle_round, log, attacker, defender)

    turn_log = {
        'nations': nations,
        'turn_score': turn_score,
        'battle_log': battle_log
    }

    return turn_log


def logs(game_path, valid_rounds):
    """
    batch reads logs from all simulations
    :param game_path: game folder path
    :param valid_rounds: list of valid rounds
    :return: log list
    """
    winners = []
    battles = []
    nations = {}

    for i in valid_rounds:
        log = parse_log(game_path=game_path, battle_round=i)
        if i == min(valid_rounds):
            nations = log['nations']  # get nation ids
        winners.append(log['turn_score'])  # get turn winner
        for j in range(len(log['battle_log'])):
            battles.append(log['battle_log'][j])  # get battle report

    log_list = {
        'nations': nations,
        'winners': winners,
        'battles': battles
    }

    return log_list
