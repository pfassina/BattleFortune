import os
import pyautogui
import subprocess
from time import sleep
from turnhandler import backupturn, restoreturn
from logparser import parsewinner, parsebattle
import psutil


def rundom(game='', switch='', nation=''):
    '''
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches, and nation being played.
    '''

    # Run Dominions on minimal settings
    program = '/k cd C:/Program Files (x86)/Steam/steamapps/common/Dominions5 & Dominions5.exe --simpgui --nosteam -waxscod' # noqa
    cmd = 'cmd ' + program + switch + ' ' + game
    process = subprocess.Popen(cmd)
    sleep(1)

    # check for autohost switch
    if switch == 'g':
        pass

        # Wait until turn is over
        done = None
        while done is None:
            if "Dominions5.exe" not in (p.name() for p in psutil.process_iter()):
                done = 'done'
                process.terminate()
            else:
                pass

    else:
        clicker(nation)

    try:
        os.system("TASKKILL /F /IM Dominions5.exe")
    except:
        pass


def clicker(nation):
    '''
    Automates Clicking within Dominions.
    Takes as input a Nation.
    '''

    # Select Nation by clicking on Nation Flag.
    nationflag = None
    while nationflag is None:
        try:
            nationflag = pyautogui.locateOnScreen(
                '.\\imgs\\' + nation + '.png')
            pyautogui.click((nationflag[0], nationflag[1]))
            sleep(1)
        except:
            pass
    sleep(1)

    # Clicks on the first "Battle" word in the message list screen.
    msg = None
    while msg is None:
        try:
            msg = pyautogui.locateOnScreen('.\\imgs\\battlemsg.png')
            pyautogui.click((msg[0], msg[1]))
            sleep(1)
        except:
            pass


def round(game, nation, turn=1):
    '''
    Run a full round of the simulation.
    Takes as input the game name, the nation, and the current simulation turn
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

    rundom(game=game, nation=nation)
    backupturn(turn)
    battle = parsebattle(turn)

    return winner, battle


def batchrun(rounds, game, nation):
    '''
    Runs X numbers of Simulation Rounds.
    Takes as input number of simultated rounds, game name, and nation.
    Outputs a disctionary with lists of parsed game logs.
    '''

    winners = []
    battles = []

    for i in range(1, rounds + 1):
        results = round(game, nation, i)
        winners.append(results[0])
        for i in range(len(results[1])):
            battles.append(results[1][i])

    output = {
        'winners': winners,
        'battles': battles
    }

    return output
