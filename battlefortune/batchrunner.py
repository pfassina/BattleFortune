import os
import pyautogui
import subprocess
from time import sleep
from turnhandler import backupturn, restoreturn
from logparser import parsewinner, parsebattle
from psutil import process_iter
import yaml


def rundom(game='', switch=''):
    '''
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches.
    '''

    dom = yaml.load(open('./battlefortune/data/config.yaml'))['dompath']

    # Run Dominions on minimal settings
    program = '/k cd ' + dom + ' & Dominions5.exe --simpgui --nosteam -waxscod'  # noqa
    cmd = 'cmd ' + program + switch + ' ' + game
    process = subprocess.Popen(cmd)
    # sleep(1)

    # check for autohost switch
    if switch == 'g':
        pass

        # Wait until turn is over
        done = None
        while done is None:
            if "Dominions5.exe" not in (p.name() for p in process_iter()):
                done = 'done'
                process.terminate()
            else:
                pass

    else:
        clicker()

    process.terminate()
    if "Dominions5.exe" in (p.name() for p in process_iter()):
        os.system("TASKKILL /F /IM Dominions5.exe")


def clicker():
    '''
    Automates Clicking within Dominions.
    Takes no input.
    '''

    # Select a Nation by clicking on the first flag.
    s = None
    while s is None:
        try:
            s = pyautogui.locateOnScreen('./battlefortune/imgs/select.png')
            pyautogui.click((s[0] + 15, s[1] + 40))
            # sleep(1)
        except:
            pass
    # sleep(1)

    # Clicks on the first "Battle" word in the message list screen.
    m = None
    while m is None:
        try:
            m = pyautogui.locateOnScreen('./battlefortune/imgs/battlemsg.png')
            pyautogui.click((m[0], m[1]))
            # sleep(1)
        except:
            pass


def round(game, turn=1):
    '''
    Run a full round of the simulation.
    Takes as input the game name, and the current simulation turn
    Returns parsed logs after a full round of simulation.

    Round sequence of events:
        1.  Restore turn backups if needed
        2.  Run Dominions on Host Mode
        3.  Backup Turn Files
        4.  Parse Win Log
        5.  Run Turn after Battle
        6.  Backup turn
        7.  Parse Battle Log
    '''

    restoreturn()
    rundom(game=game, switch='g')
    backupturn(turn)
    winner = parsewinner(turn)

    rundom(game=game)
    backupturn(turn)
    battle = parsebattle(turn)

    return winner, battle


def batchrun(rounds, game):
    '''
    Runs X numbers of Simulation Rounds.
    Takes as input number of simultated rounds, game name.
    Outputs a dictionary with lists of parsed game logs.
    '''

    winners = []
    battles = []

    for i in range(1, rounds + 1):
        results = round(game, i)
        winners.append(results[0])
        for i in range(len(results[1])):
            battles.append(results[1][i])

    output = {
        'winners': winners,
        'battles': battles
    }

    return output
