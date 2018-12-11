import os
import shutil
import yaml


def backupturn(turn):
    '''
    Backups turn and log files.
    Takes as input the simulation turn number.
    '''

    gamepath = yaml.load(open('config.yaml'))['gamepath']
    files = [f for f in os.listdir(gamepath) if os.path.isfile(os.path.join(
        gamepath, f)) and f.endswith('.trn') or f.endswith('.2h') or f == 'ftherlnd']

    if not os.path.exists(gamepath + 'turns\\'):
        os.makedirs(gamepath + 'turns\\')

    for file in files:
        src = gamepath + file
        dst = gamepath + 'turns\\' + str(turn) + '_' + file
        shutil.copy(src, dst)

    try:
        dompath = yaml.load(open('config.yaml'))['dompath']
        log = dompath + 'log.txt'
        shutil.copy(log, gamepath + 'turns\\' + str(turn) + '_log.txt')

    except:
        pass


def restoreturn():
    '''
    Restores Pre-Battle turn 0.
    '''

    gamepath = yaml.load(open('config.yaml'))['gamepath']
    files = [f for f in os.listdir(
        gamepath + 'turns\\') if os.path.isfile(os.path.join(gamepath + 'turns\\', f)) and f.startswith('0_')]

    for file in files:
        src = gamepath + 'turns\\' + file
        dst = gamepath + file[2:len(file)]
        shutil.copy(src, dst)
