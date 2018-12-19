import keyboard
from logparser import parselog, confirm_log
import os
from psutil import process_iter
from pyautogui import locateOnScreen, click
import subprocess
from turnhandler import backupturn, restoreturn
import yaml


def clicker():
    '''
    Finds and clicks on Nation Flag.
    '''

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

    keyboard.press_and_release('esc')  # exit messages
    keyboard.press_and_release('g')  # go to screen
    keyboard.write(str(province))  # select province
    keyboard.press_and_release('enter')  # confirm
    keyboard.press_and_release('c')  # view casualities
    keyboard.press_and_release('esc')  # back to map
    keyboard.press_and_release('d')  # try to add PD


def rundom(province, game='', switch=''):
    '''
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches.
    '''

    dom = yaml.load(open('./battlefortune/data/config.yaml'))['dompath']

    # Run Dominions on minimal settings
    switches = ' --simpgui --nosteam -waxsco' + switch + ' '
    program = '/k cd /d' + dom + ' & Dominions5.exe'
    cmd = 'cmd ' + program + switches + game
    process = subprocess.Popen(cmd)

    # if auto hosting battle
    if switch == 'g -T':
        pass

        # Wait until turn is over
        done = None
        while done is None:
            if "Dominions5.exe" not in (p.name() for p in process_iter()):
                done = 'done'
                process.terminate()
    else:
        clicker()  # select nation
        gotoprov(dom, province)  # check battle report
        confirm_log(dom)  # validate log

    process.terminate()
    if "Dominions5.exe" in (p.name() for p in process_iter()):
        os.system("TASKKILL /F /IM Dominions5.exe")


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

    restoreturn()  # restore back-up files if needed
    rundom(province=province, game=game, switch='g -T')  # auto host battle
    rundom(province=province, game=game, switch='d')  # generate battle logs
    backupturn(turn)  # back-up turn files
    turn_log = parselog(turn)  # read and parse battle log

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
        log = round(game, province, i)  # get turn log
        if i == 1:
            nations = log['nations']  # get nation ids
        winners.append(log['turn_score'])  # get turn winner
        for j in range(len(log['battlelog'])):
            battles.append(log['battlelog'][j])  # get battle report
        print('Round: ' + str(i))

    output = {
        'nations': nations,
        'winners': winners,
        'battles': battles
    }

    return output
