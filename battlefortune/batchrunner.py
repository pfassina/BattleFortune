import keyboard
from logparser import parselog, validate_log
import os
from psutil import process_iter
from pyautogui import locateOnScreen, click
import subprocess
from turnhandler import backupturn, clonegame, cleanturns, delete_log
import yaml
from time import sleep
import threading
import time
import win32gui


failed_rounds = []


def wait_screen_load(path):
    """
    Waits Nation Selection screen to load
    :param path: dominions log path
    :return: True if load was complete
    """

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
    Selects the first Nation on Nation selection screen.
    :return: True if Dominions window handle was found.
    """

    # Loop until Dominions Window Handle is found
    hwnd = 0
    while hwnd == 0:
        hwnd = win32gui.FindWindow(None, 'Dominions 5')

    # Get Dominions Windows Coordinates
    x, y = win32gui.ClientToScreen(hwnd, (0, 0))

    # Move cursor by 400x280 to select first Nation
    click((x + 400, y + 280))

    return True


def go_to_province(province):
    """
    Automates keyboard shortcuts to generate log.
    :param province: Province number where battle occurs
    :return: True when all commands were executed
    """

    keyboard.press_and_release('esc')  # exit messages
    keyboard.press_and_release('g')  # go to screen
    keyboard.write(str(province))  # select province
    keyboard.press_and_release('enter')  # confirm
    keyboard.press_and_release('c')  # view casualities
    keyboard.press_and_release('esc')  # back to map
    keyboard.press_and_release('d')  # try to add PD

    return True


def wait_host(path, start_time):
    """
    Waits Dominions to Host battle.
    :param path: dominions game path
    :param start_time: Time when ftherlnd was last updated
    :return: True if ftherlnd was updated
    """

    # Loop until host is finished
    done = False
    before_host_check = int(round(time.time() * 1000))
    while done is False:
        # check if ftherlnd was updated
        ftherlnd_update_time = os.path.getmtime(path + 'ftherlnd')
        if ftherlnd_update_time > start_time:
            done = True
            break
        # break if host duration greater than 35 seconds
        last_host_check = int(round(time.time() * 1000))
        hosting_duration = (last_host_check - before_host_check)/1000
        if hosting_duration > 35:
            break

        sleep(1)  # sleep 1 second between checks

    return done


def run_dominions(province, game='', switch='', turn=-1):
    """
    Runs Dominions.
    :param province: Province where battle occurs
    :param game: Name of the game being simulated
    :param switch: Additional Dominions switches
    :param turn: Turn of the simulation
    :return: True after process is terminated
    """

    global failed_rounds

    # Get Paths
    with open('./battlefortune/data/config.yaml') as file:
        paths = yaml.load(file)

    dpath = paths['dompath']
    gpath = paths['gamepath']
    
    if turn > -1:
        idx = gpath.rfind("/")
        gpath = gpath[:idx] + str(turn) + gpath[idx:]
        game = game + str(turn)

    start_time = os.path.getmtime(gpath + 'ftherlnd')  # ftherlnd last update

    # Run Dominions on minimal settings
    switches = ' --simpgui --nosteam --res 960 720 -waxsco' + switch + ' '
    program = '/k cd /d' + dpath + ' & Dominions5.exe'
    cmd = 'cmd ' + program + switches + game

    process = subprocess.Popen(cmd)  # run Dominions

    if switch == 'g -T':  # if auto hosting battle

        success = wait_host(path=gpath, start_time=start_time)
        if not success:
            failed_rounds.append(turn)

    else:
        # Generate Log
        wait_screen_load(dpath)  # wait nation selection screen to load
        sleep(1)
        select_nation()  # select first nation
        go_to_province(province)  # check battle report

        # Validate Round
        valid = validate_log(dpath)  # validate log
        if not valid:
            failed_rounds.append(turn)

    # Terminate process
    process.kill()
    if switch != 'g -T':
        if "Dominions5.exe" in (p.name() for p in process_iter()):
            os.system("TASKKILL /F /IM Dominions5.exe")

    return True


def host_battle(game, province, rounds):
    """"
    Host games concurrently based on the number of threads.
    :param game: game name
    :param province: province where battle occurs
    :param rounds: number of rounds to be hosted
    """

    switch = 'g -T'
    threads = []

    max_threads = yaml.load(open('./battlefortune/data/config.yaml'))['maxthreads']

    start_range = 1
    end_range = start_range + max_threads
    if end_range > (rounds + 1):
        end_range = rounds + 1

    while start_range < (rounds + 1):
        for i in range(start_range, end_range):
            t = threading.Thread(target=run_dominions, args=(province, game, switch, i))
            threads.append(t)
            t.start()

        for thread in threads:
            thread.join()

        threads = []
        start_range = start_range + max_threads
        end_range = end_range + max_threads
        if end_range > (rounds + 1):
            end_range = rounds + 1


def finalize_turn(game, province, turn=1):
    """
    Generates the log for each simulation round, one at a time.
    :param game: name of the game to be hosted
    :param province: number of the province where battle occurs
    :param turn: number of the simulation round
    :return: turn log
    """

    global failed_rounds

    run_dominions(province=province, game=game, switch='d', turn=turn)  # generate battle logs

    turn_log = {}

    if turn not in failed_rounds:
        backupturn(turn)  # back-up turn files
        turn_log = parselog(turn)  # read and parse battle log

    # delete log
    delete_log()

    return turn_log


def batchrun(rounds, game, province):
    """
    Runs X numbers of Simulation Rounds.
    Takes as input number of simulated rounds, game name.
    Outputs a dictionary with lists of parsed game logs.
    """

    global failed_rounds
    winners = []
    battles = []
    nations = {}

    for i in range(1, rounds + 1):
        clonegame(i)

    host_battle(game, province, rounds)

    for i in range(1, rounds + 1):

        if i in failed_rounds:
            continue

        log = finalize_turn(game, province, i)  # get turn log
        if i in failed_rounds:
            continue

        nations = log['nations']  # get nation ids
        winners.append(log['turn_score'])  # get turn winner
        for j in range(len(log['battlelog'])):
            battles.append(log['battlelog'][j])  # get battle report
        print('Round: ' + str(i))

    cleanturns(rounds)
    failed_rounds = []

    output = {
        'nations': nations,
        'winners': winners,
        'battles': battles
    }

    return output
