import os
import pyautogui
import subprocess
from time import sleep
from turnhandler import backupturn, restoreturn
from logparser import parsewinner, parsebattle
import psutil
from calc import battlecalc, wincalc

def clicker(nation):

    nationflag = None
    while nationflag is None:
        try:
            nationflag = pyautogui.locateOnScreen('.\\imgs\\' + nation + '.png')
            pyautogui.click((nationflag[0], nationflag[1]))
            sleep(1)
        except:
             pass

    sleep(1)
    msg = None
    while msg is None:
        try:
            msg = pyautogui.locateOnScreen('.\\imgs\\battlemsg.png')
            pyautogui.click((msg[0], msg[1]))
            sleep(1)
        except:
             pass


def rundom(game='', switch='', nation=''):

    program = '/k cd C:/Program Files (x86)/Steam/steamapps/common/Dominions5 & Dominions5.exe --simpgui --nosteam -waxscod'
    cmd = 'cmd ' + program + switch + ' ' + game
    process = subprocess.Popen(cmd)
    sleep(1)

    if switch == 'g':
        pass

        done = None
        while done == None:
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


def round(game, nation, turn=1):

    # backupturn(0)
    restoreturn()

    rundom(game=game, switch='g')
    backupturn(turn)
    winner = parsewinner(turn)

    rundom(game=game, nation=nation)
    backupturn(turn)
    battle = parsebattle(turn)

    return winner, battle


def main(rounds):

    winners = []
    battles = []

    for i in range(1, rounds + 1):
        results = round('test', 'atlantis', i)
        winners.append(results[0])
        for i in range(len(results[1])):
            battles.append(results[1][i])

    return {'winners': winners, 'battles': battles}

# results = main(2)
# winners = results['winners']
# battles = results['battles']
#
# print(wincalc(winners))
# print(battlecalc(battles))
