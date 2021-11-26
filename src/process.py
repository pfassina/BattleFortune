import os
import Quartz
import signal

import keyboard
import pyautogui

from src import read, utility, globals


def wait_screen_load():
    """
    Waits Nation Selection screen to load
    """

    valid = False
    while valid is False:
        try:
            with open(os.path.join(globals.DOM_PATH, 'log.txt'), 'r') as file:
                blurb = file.read()
                load_complete = blurb.rfind('playturn: autohost')  # battle loaded
        except FileNotFoundError:
            continue
        if load_complete == -1:
            continue
        if load_complete != -1:
            valid = True


def select_nation():
    """
    Selects the first Nation on Nation selection screen.
    """

    x, y = (0, 0)
    apps = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly & Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    for app in apps:
        if app.get('kCGWindowOwnerName') == 'dom5_mac' and app.get('kCGWindowIsOnscreen') == 1:
            window = app.get('kCGWindowBounds')
            x, y = window.get('X'), window.get('Y') + 25
        else:
            pass

    # Move cursor by 400x280 to select first Nation
    pyautogui.click((x + 500, y + 355))


def go_to_province():
    """
    Automates keyboard shortcuts to generate log.
    """

    keyboard.press_and_release('esc')  # exit messages
    keyboard.press_and_release('g')  # go to screen
    keyboard.write(str(globals.PROVINCE))  # select province
    keyboard.press_and_release('enter')  # confirm
    keyboard.press_and_release('c')  # view results
    keyboard.press_and_release('esc')  # back to map
    keyboard.press_and_release('d')  # try to add PD


def validate_round(simulation_round):
    """
    Check if round generated a valid log
    :param simulation_round: simulation round number
    """

    valid = read.validate_log()  # validate log

    if not valid:
        globals.VALID_ROUNDS.remove(simulation_round)
        globals.FAILED_ROUNDS.append(simulation_round)


def rounds(simulation_round, process_id):
    """
    Clicks through a Dominions game to generate log
    :return: True if successful
    """

    # wait nation selection screen to load
    wait_screen_load()

    # select first nation
    select_nation()

    # check battle report
    go_to_province()

    # validate round
    validate_round(simulation_round)

    # terminate process
    os.kill(process_id, signal.SIGTERM)

    # move log to round folder
    utility.move_log(simulation_round)
