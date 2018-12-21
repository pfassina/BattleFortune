import keyboard
from logparser import parselog, validate_log
import os
from psutil import process_iter
from pyautogui import locateOnScreen, click
import subprocess
from turnhandler import backupturn, restoreturn, clonegame
import yaml
from time import sleep
import threading


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


def wait_host(path, start):
    '''
    Waits Dominions Autohost to Host.
    Checks for Fatherlnd update.
    '''

    print("wait_host, path: " + path)
    print("wait_host, start: " + str(start))
    done = False
    while done is False:
        print("wait_host, still waiting for path " + path)
        sleep(1)
        end = os.path.getmtime(path + 'ftherlnd')
        if end > start:
            done = True
            break
        else:
            continue

    return done


def rundom(province, game='', switch='', turn=-1):
    '''
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches.
    '''
    print("called rundom for turn " + str(turn))

    # Get Paths
    with open('./battlefortune/data/config.yaml') as file:
        paths = yaml.load(file)

    dpath = paths['dompath']
    gpath = paths['gamepath']

    if turn > -1:
        idx = gpath.rfind("/")
        gpath = gpath[:idx] + str(turn) + gpath[idx:]
        game = game + str(turn)

    print("gpath: " + gpath)
    start = os.path.getmtime(gpath + 'ftherlnd')  # ftherlnd last update

    # Run Dominions on minimal settings
    switches = ' --simpgui --nosteam -waxsco' + switch + ' '
    program = '/k cd /d' + dpath + ' & Dominions5.exe'
    cmd = 'cmd ' + program + switches + game

    print("about to open process for cmd: " + cmd)
    process = subprocess.Popen(cmd)

    if switch == 'g -T':  # if auto hosting battle

        wait_host(gpath, start)
        print("hosting done for turn " + str(turn))

    else:
        clicker()  # select nation
        gotoprov(dpath, province)  # check battle report
        validate_log(dpath)  # validate log

    process.terminate()

    if switch != 'g -T':
        if "Dominions5.exe" in (p.name() for p in process_iter()):
            os.system("TASKKILL /F /IM Dominions5.exe")


def prepareTurn(turn=1):
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

    print("called prepareTurn")
    clonegame(turn)
    restoreturn(turn)  # restore back-up files if needed


def host(game, province, rounds):

    print("called host")
    switch = 'g -T'
    threads = []

    for i in range(1, rounds + 1):
        # auto host battle
        t = threading.Thread(target=rundom, args=(province, game, switch, i))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def finalizeTurn(game, province, turn=1):
    print("called finalizeTurn")
    # generate battle logs
    rundom(province=province, game=game, switch='d', turn=turn)
    backupturn(turn)  # back-up turn files
    turn_log = parselog(turn)  # read and parse battle log

    return turn_log


def batchrun(rounds, game, province):
    '''
    Runs X numbers of Simulation Rounds.
    Takes as input number of simultated rounds, game name.
    Outputs a dictionary with lists of parsed game logs.
    '''
    print("called batchrun")

    winners = []
    battles = []

    for i in range(1, rounds + 1):
        prepareTurn(i)

    host(game, province, rounds)

    for i in range(1, rounds + 1):
        log = finalizeTurn(game, province, i)  # get turn log
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
