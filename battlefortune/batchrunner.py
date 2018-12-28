import keyboard
from logparser import parselog, validate_log
import os
from psutil import process_iter
from pyautogui import locateOnScreen, click
import subprocess
from turnhandler import backupturn, restoreturn
import yaml
import win32gui


def wait_screen_load(path):

    valid = False

    i = 0
    while i < 1000000:
        try:
            with open(path + 'log.txt') as file:
                blurb = file.read()
                load_complete = blurb.rfind('playturn: autohost')  # battle loaded
                if load_complete == -1:
                    i += 1
                    continue
                if load_complete != -1:  # Player Won
                    valid = True
                    break
        except FileNotFoundError:
            i += 1
    return valid


def select_nation():
    """
    Find Dominions Window and Clicks Selects First Nation.
    """

    hwnd = 0
    while hwnd is 0:
        hwnd = win32gui.FindWindow(None, 'Dominions 5')

    x, y = win32gui.ClientToScreen(hwnd, (0, 0))

    click((x + 400, y + 280))


def go_to_prov(path, province):
    """
    Automates keyboard shortcuts to generate log.
    Takes as input the path to dominions log, and the province number.
    """

    keyboard.press_and_release('esc')  # exit messages
    keyboard.press_and_release('g')  # go to screen
    keyboard.write(str(province))  # select province
    keyboard.press_and_release('enter')  # confirm
    keyboard.press_and_release('c')  # view casualities
    keyboard.press_and_release('esc')  # back to map
    keyboard.press_and_release('d')  # try to add PD


def wait_host(path, start):
    """
    Waits Dominions Autohost to Host.
    Checks for Fatherlnd update.
    """

    done = False
    while done is False:
        end = os.path.getmtime(path + 'ftherlnd')
        if end > start:
            done = True
            break
        else:
            continue

    return done


def rundom(province, game='', switch=''):
    """
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches.
    """

    # Get Paths
    with open('./battlefortune/data/config.yaml') as file:
        paths = yaml.load(file)

    dpath = paths['dompath']
    gpath = paths['gamepath']
    start = os.path.getmtime(gpath + 'ftherlnd')  # ftherlnd last update

    # Run Dominions on minimal settings
    switches = ' --simpgui --nosteam --res 960 720 -waxsco' + switch + ' '
    program = '/k cd /d' + dpath + ' & Dominions5.exe'
    cmd = 'cmd ' + program + switches + game

    process = subprocess.Popen(cmd)

    if switch == 'g -T':  # if auto hosting battle

        wait_host(gpath, start)

    else:
        wait_screen_load(dpath)
        select_nation()  # select nation
        go_to_prov(dpath, province)  # check battle report
        validate_log(dpath)  # validate log

    process.terminate()
    if "Dominions5.exe" in (p.name() for p in process_iter()):
        os.system("TASKKILL /F /IM Dominions5.exe")


def round(game, province, turn=1):
    """
    Run a full round of the simulation.
    Takes as input the game name, and the current simulation turn
    Returns parsed logs after a full round of simulation.

    Round sequence of events:
        1.  Restore turn backups if needed
        2.  Run Dominions on Host Mode
        5.  Run Turn after Battle
        6.  Backup turn tiles
        7.  Parse Battle Log
    """

    restoreturn()  # restore back-up files if needed
    rundom(province=province, game=game, switch='g -T')  # auto host battle
    rundom(province=province, game=game, switch='d')  # generate battle logs
    backupturn(turn)  # back-up turn files
    turn_log = parselog(turn)  # read and parse battle log

    return turn_log


def batchrun(rounds, game, province):
    """
    Runs X numbers of Simulation Rounds.
    Takes as input number of simultated rounds, game name.
    Outputs a dictionary with lists of parsed game logs.
    """

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
