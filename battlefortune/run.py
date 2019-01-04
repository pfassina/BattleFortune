import os
import subprocess
import threading

import keyboard
from pyautogui import click
import win32gui
import win32con

import read
import prepare

failed_rounds = []


# RUN DOMINIONS
def run_dominions(path, game, host=False):
    """
    Run command for Dominions
    :param path: dominions executable path
    :param game: game name
    :param host: True to host battle
    :return: run process
    """

    if host:
        switches = ' --simpgui --nosteam --res 960 720 -waxscog -T '
    else:
        switches = ' --simpgui --nosteam --res 960 720 -waxscod '

    program = '/k cd /d' + path + ' & Dominions5.exe'
    cmd = 'cmd ' + program + switches + game

    process = subprocess.Popen(cmd)  # run Dominions

    return process


# HOST BATTLES
def host(dom_path, game_path, game, battle_round):
    """
    host battle for a single round
    :param dom_path: dominions folder path
    :param game_path: game folder path
    :param game: game name
    :param battle_round: simulation round
    :return: True if successful
    """
    global failed_rounds

    start_time = os.path.getmtime(game_path + 'ftherlnd')
    process = run_dominions(path=dom_path, game=game, host=True)
    success = validate_host(path=game_path, start_time=start_time)

    if not success:
        failed_rounds.append(battle_round)

    os.system("TASKKILL /F /T /PID %i" % process.pid)

    return True


def validate_host(path, start_time):
    """
    Waits Dominions to Host battle.
    :param path: dominions game path
    :param start_time: Time when ftherlnd was last updated
    :return: True if ftherlnd was updated
    """

    # Loop until host is finished
    done = False
    while done is False:
        # check if ftherlnd was updated
        ftherlnd_update_time = os.path.getmtime(path + 'ftherlnd')
        if ftherlnd_update_time > start_time:
            done = True
            break
        # check for host error
        hwnd = win32gui.FindWindow(None, 'NÃ¥got gick fel!')
        if hwnd > 0:
            win32gui.SetForegroundWindow(hwnd)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            break

    return done


def batch_host(dom_path, game_path, game, rounds):
    """"
    Host games concurrently based on the number of threads.
    :param game_path: game folder path
    :param dom_path: dominions folder path
    :param game: game name
    :param rounds: number of rounds to be hosted
    """

    threads = []
    for i in range(1, rounds + 1):

        kwargs = {
            'dom_path': dom_path,
            'game_path': game_path[:-1] + str(i) + '/',
            'game': game + str(i),
            'battle_round': i
        }

        t = threading.Thread(target=host, kwargs=kwargs)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    return True


# GENERATE LOG
def wait_screen_load(path):
    """
    Waits Nation Selection screen to load
    :param path: dominions log path
    :return: True if load was complete
    """

    log = path + 'log.txt'

    valid = False
    while valid is False:
        try:
            with open(log, mode='r') as file:
                blurb = file.read()
        except FileNotFoundError:
            continue
        try:
            load_complete = blurb.rfind('playturn: autohost')  # battle loaded
        except PermissionError:
            continue
        if load_complete == -1:
            continue
        if load_complete != -1:
            valid = True
            break

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
    keyboard.press_and_release('c')  # view results
    keyboard.press_and_release('esc')  # back to map
    keyboard.press_and_release('d')  # try to add PD

    return True


def batch_click(dom_path, game_path, game, rounds, province):
    """
    Clicks through a Dominions game to generate log
    :param dom_path: dominions folder path
    :param game_path: game folder path
    :param game: game name
    :param rounds: total number of simulation rounds
    :param province: province where battle occurs
    :return: True if successful
    """
    global failed_rounds

    for i in range(1, rounds + 1):

        run_args = {
            'path': dom_path,
            'game': game + str(i)
        }

        process = run_dominions(**run_args)

        wait_screen_load(dom_path)  # wait nation selection screen to load
        select_nation()  # select first nation
        go_to_province(province)  # check battle report

        # Validate Round
        valid = read.validate_log(dom_path)  # validate log
        if not valid:
            failed_rounds.append(i)

        # Terminate process
        os.system("TASKKILL /F /T /PID %i" % process.pid)

        # Move Log to Round Folder
        round_path = game_path[:-1] + str(i) + '/'
        prepare.move_log(dom_path, round_path)

        print('Round: ' + str(i))

    return True


def simulation(dom_path, game_path, temp_path, game, rounds, province):
    """
    Runs X numbers of Simulation Rounds.
    :param temp_path: Dominions temporary folder path
    :param game_path: Game folder path
    :param dom_path: Dominions folder path
    :param rounds: Number of rounds to be simulated
    :param game: game name that will be simulated
    :param province: province number where battle occurs
    :return: list of parsed logs
    """

    # Delete all temporary files to prevent errors
    try:
        prepare.delete_temp(path=temp_path)
    except FileNotFoundError:
        pass

    # Batch Host all simulations
    host_completed = batch_host(dom_path=dom_path, game_path=game_path, game=game, rounds=rounds)
    assert host_completed, 'Host Failed'

    # Batch Click all games to generate logs
    click_completed = batch_click(dom_path=dom_path, game_path=game_path, game=game, rounds=rounds, province=province)
    assert click_completed, 'Click Failed'

    # Remove failed rounds
    global failed_rounds
    simulations = list(range(1, rounds + 1))
    valid_rounds = [x for x in simulations if x not in failed_rounds]

    # Parse logs
    log_list = read.logs(game_path, valid_rounds)
    assert log_list['nations'], 'nation log not captured'
    assert log_list['winners'], 'winners log not captured'
    assert log_list['battles'], 'battles log not captured'

    # Remove Simulation files
    prepare.clean_turns(rounds)

    return log_list
