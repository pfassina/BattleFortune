import keyboard
from logparser import parselog
import os
from psutil import process_iter
from pyautogui import locateOnScreen, click
import subprocess
from turnhandler import backupturn, restoreturn
import yaml
from time import sleep

def rundom(province, game='', switch=''):
    '''
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches.
    '''

    dom = yaml.load(open('./battlefortune/data/config.yaml'))['dompath']

    # Run Dominions on minimal settings
    program = '/k cd /d' + dom + ' & Dominions5.exe --simpgui --nosteam -waxsco'  # noqa
    cmd = 'cmd ' + program + switch + ' ' + game
    process = subprocess.Popen(cmd)

    # check for autohost switch
    if switch == 'g -T':
        pass

        # Wait until turn is over
        done = None
        while done is None:
            if "Dominions5.exe" not in (p.name() for p in process_iter()):
                done = 'done'
                process.terminate()
    else:
        clicker()
        gotoprov(dom, province)

    process.terminate()
    if "Dominions5.exe" in (p.name() for p in process_iter()):
        os.system("TASKKILL /F /IM Dominions5.exe")


def clicker():
    '''
    Automates Clicking within Dominions.
    '''

    # Select a Nation by clicking on the first flag.
    s = None
    while s is None:
        try:
            select = './battlefortune/imgs/select.png'
            s_region = (800, 400, 100, 100)
            s = locateOnScreen(select, region=s_region, grayscale=True)

        except RuntimeError:
            print('Unable to select Nation.')

    click((s[0] + 15, s[1] + 40))


def gotoprov(path, province):
    '''
    Automates keyboard shortcuts to generate log.
    Takes as input the path to dominions log, and the province number.
    '''
    # sleep(1)
    keyboard.press_and_release('esc')
    keyboard.press_and_release('g')
    keyboard.write(str(province))
    keyboard.press_and_release('enter')
    keyboard.press_and_release('c')
    keyboard.press_and_release('esc')
    keyboard.press_and_release('d')
    sleep(2)


def round(game, province, turn=1):
    '''
    Run a full round of the simulation.
    Takes as input the game name, and the current simulation turn
    Returns parsed logs after a full round of simulation.

    Round sequence of events:
        1.  Restore turn backups if needed
        2.  Run Dominions on Host Mode
        5.  Run Turn after Battle
        6.  Backup turn tiles
        7.  Parse Battle Log
    '''

    restoreturn()
    rundom(province=province, game=game, switch='g -T')
    rundom(province=province, game=game, switch='d')
    backupturn(turn)
    turn_log = parselog(turn)

    return turn_log


def batchrun(rounds, game, province):
    '''
    Runs X numbers of Simulation Rounds.
    Takes as input number of simultated rounds, game name.
    Outputs a dictionary with lists of parsed game logs.
    '''

    winners = []
    battles = []

    for i in range(1, rounds + 1):
        log = round(game, province, i)
        if i == 1:
            nations = log['nations']
        winners.append(log['turn_score'])
        for j in range(len(log['battlelog'])):
            battles.append(log['battlelog'][j])
        print('Round: ' + str(i))

    output = {
        'nations': nations,
        'winners': winners,
        'battles': battles
    }

    return output
