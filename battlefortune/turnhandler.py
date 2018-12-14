import os
import shutil
import yaml


def backupturn(turn):
    '''
    Backups turn and log files.
    Takes as input the simulation turn number.
    '''

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']

    if not os.path.exists(path + 'turns/'):
        os.makedirs(path + 'turns/')

    dir = os.listdir(path)
    files = [f for f in dir if f.endswith(('.trn', '.2h')) or f == 'ftherlnd']

    if len(files) > 0:

        for file in files:
            src = path + file
            dst = path + 'turns/' + str(turn) + '_' + file
            shutil.copy(src, dst)

    dom = yaml.load(open('./battlefortune/data/config.yaml'))['dompath']
    log = dom + 'log.txt'
    shutil.copy(log, path + 'turns/' + str(turn) + '_log.txt')


def restoreturn():
    '''
    Restores Pre-Battle turn 0.
    '''

    path = yaml.load(open('./battlefortune/data/config.yaml'))['gamepath']

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
            src = path + file
            dst = path + 'turns/0_' + file
            shutil.copy(src, dst)
