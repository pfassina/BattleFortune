import os
import shutil
from pathlib import Path


def backupturn(turn):

    home = str(Path.home()) + '\\AppData\\Roaming\\Dominions5\\savedgames\\test\\'
    files = [f for f in os.listdir(home) if os.path.isfile(os.path.join(home, f)) and f.endswith('.trn') or f.endswith('.2h') or f == 'ftherlnd']

    if not os.path.exists(home + 'turns\\'):
        os.makedirs(home + 'turns\\')

    for file in files:
        src = home + file
        dst = home + '\\turns\\' + str(turn) + '_' + file
        shutil.copy(src, dst)

    try:

        log = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Dominions5\\log.txt'
        shutil.copy(log, home + '\\turns\\' + str(turn) + '_log.txt')

    except:
        pass


def restoreturn():

    home = str(Path.home()) + '\\AppData\\Roaming\\Dominions5\\savedgames\\test\\'
    files = [f for f in os.listdir(home + 'turns\\') if os.path.isfile(os.path.join(home + 'turns\\', f)) and f.startswith('0_')]

    for file in files:
        src = home + '\\turns\\' + file
        dst = home + file[2:len(file)]
        shutil.copy(src, dst)
