import os
import shutil
import yaml


def backupturn(turn):
    '''
    Backups turn and log files.
    Takes as input the simulation turn number.
    '''

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


def restoreturn(turn=-1):
    '''
    Restores Pre-Battle turn 0.
    '''

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']
    if turn > -1:
        idx = path.rfind("/")
        path = path[:idx] + str(turn) + path[idx:]

    if not os.path.exists(path + 'turns/'):
        os.makedirs(path + 'turns/')

    dir = os.listdir(path + 'turns/')
    files = [f for f in dir if f.startswith('0_')]

    if len(files) > 0:

        for file in files:
            src = path + 'turns/' + file
            dst = path + file[2:len(file)]
            shutil.copy(src, dst)
    else:
        for file in os.listdir(path):
            if os.path.isfile(path + file):
                src = path + file
                dst = path + 'turns/0_' + file
                print("src: " + src)
                print("dst: " + dst)
                shutil.copy(src, dst)


def clonegame(turn):
    '''
    Creates clone of game to analyze for turn.
    '''

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']
    idx = path.rfind("/")
    turnpath = path[:idx] + str(turn) + path[idx:]

    print("turn path: " + turnpath)

    if not os.path.exists(turnpath):
        os.makedirs(turnpath)

    folder = os.listdir(path)
    files = [f for f in folder]
    print("path: " + path)
    print("files: " + str(len(files)))
    if len(files) > 0:
        for file in files:
            print("file: " + file)
            if os.path.isfile(path + file):
                src = path + file
                dst = turnpath + file
                print("clone src: " + src)
                print("clone dst: " + dst)
                shutil.copy(src, dst)
