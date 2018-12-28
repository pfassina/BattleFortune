import os
import shutil
import yaml


def backupturn(turn):
    """
    Backups turn and log files.
    :param turn: Simulation round.
    :return: True when files are backed-up
    """

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']

    # Create Turn Folder
    if not os.path.exists(path + 'turns/'):
        os.makedirs(path + 'turns/')

    dir = os.listdir(path)
    files = [f for f in dir if f.endswith(('.trn', '.2h')) or f == 'ftherlnd']

    # Backlog Turn Files
    if len(files) > 0:

        for file in files:
            src = path + file
            dst = path + 'turns/' + str(turn) + '_' + file
            shutil.copy(src, dst)

    # Backlog Log file
    dom = yaml.load(open('./battlefortune/data/config.yaml'))['dompath']
    log = dom + 'log.txt'
    shutil.copy(log, path + 'turns/' + str(turn) + '_log.txt')

    return True


def cleanturns(rounds):
    """
    Cleans up temporary folders
    :param rounds: number of simulation rounds
    :return: True when temporary turn files are removed.
    """

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']
    idx = path.rfind("/")
    
    for i in range(1, rounds + 1):
        folder = path[:idx] + str(i) + path[idx:]
        shutil.rmtree(folder)
    
    turnspath = path + "turns"
    shutil.rmtree(turnspath)

    return True


def clonegame(turn):
    """
    Clones game files for each round.
    :param turn: simulation round
    :return: True when all files were cloned
    """

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']
    idx = path.rfind("/")
    turn_path = path[:idx] + str(turn) + path[idx:]
    
    print("turn path: " + turn_path)
    
    if not os.path.exists(turn_path):
        os.makedirs(turn_path)
        
    folder = os.listdir(path)
    files = [f for f in folder]
    print("path: " + path)
    print("files: " + str(len(files)))
    if len(files) > 0:
        for file in files:
            print("file: " + file)
            if os.path.isfile(path + file):
                src = path + file
                dst = turn_path + file
                print("clone src: " + src)
                print("clone dst: " + dst)
                shutil.copy(src, dst)

    return True


def delete_log():
    """
    Delete Log file.
    :return: True when log is deleted.
    """
    dom = yaml.load(open('./battlefortune/data/config.yaml'))['dompath']
    log = dom + 'log.txt'
    os.remove(log)

    return True
