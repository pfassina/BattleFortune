import os
import Quartz
import signal

import keyboard
import pyautogui

from src import utility
from src.config import SimConfig


def wait_screen_load(dominions_path: str) -> None:
    """
    Waits Nation Selection screen to load
    """

    log_path = os.path.join(dominions_path, 'log.txt')
    while not os.path.exists(log_path):
        continue

    with open(log_path, 'r') as log:

        load_complete = -1
        while load_complete == -1:
            blurb = log.read()
            load_complete = blurb.rfind('playturn: autohost')


def select_nation() -> None:
    """
    Selects the first Nation on Nation selection screen.
    """

    apps = Quartz.CGWindowListCopyWindowInfo(  # type: ignore
        Quartz.kCGWindowListOptionOnScreenOnly  # type: ignore
        & Quartz.kCGWindowListExcludeDesktopElements,  # type: ignore
        Quartz.kCGNullWindowID)  # type: ignore

    for app in apps:

        if app.get('kCGWindowOwnerName') != 'dom5_mac':
            continue

        if app.get('kCGWindowIsOnscreen') != 1:
            continue

        window = app.get('kCGWindowBounds')
        x, y = window.get('X'), window.get('Y') + 25
        pyautogui.click((x + 500, y + 355))
        break


def go_to_province(province: int) -> None:
    """
    Automates keyboard shortcuts to generate log.
    """

    keyboard.press_and_release('esc')  # exit messages
    keyboard.press_and_release('g')  # go to screen
    keyboard.write(str(province))  # select province
    keyboard.press_and_release('enter')  # confirm
    keyboard.press_and_release('c')  # view results
    keyboard.press_and_release('esc')  # back to map
    keyboard.press_and_release('d')  # try to add PD


def rounds(config: SimConfig, simulation_round: int, process_id: int) -> None:
    """
    Clicks through a Dominions game to generate log
    :return: True if successful
    """

    # wait nation selection screen to load
    wait_screen_load(config.dominions_path)

    # select first nation
    select_nation()

    # check battle report
    go_to_province(config.province)

    # terminate process
    os.kill(process_id, signal.SIGTERM)

    # move log to round folder
    utility.move_log(config, simulation_round)
