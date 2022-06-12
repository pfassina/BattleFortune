from dataclasses import dataclass
import os
import Quartz
import signal

import keyboard
import pyautogui

from src.config import SimConfig


@dataclass
class AppWindow:
    x: int
    y: int

    @property
    def banner_position(self) -> tuple[int, int]:
        banner_x = self.x + 500
        banner_y = self.y + 25 + 355  # header + y delta
        return (banner_x, banner_y)


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


def get_app_window() -> AppWindow:

    apps = Quartz.CGWindowListCopyWindowInfo(  # type: ignore
        Quartz.kCGWindowListOptionOnScreenOnly  # type: ignore
        & Quartz.kCGWindowListExcludeDesktopElements,  # type: ignore
        Quartz.kCGNullWindowID)  # type: ignore

    dom_5_apps = (a for a in apps if a.get('kCGWindowOwnerName') == 'dom5_mac')
    dom_5 = next(a for a in dom_5_apps if a.get('kCGWindowIsOnscreen') == 1)
    window = dom_5.get('kCGWindowBounds')

    return AppWindow(window['X'], window['Y'])


def select_nation() -> None:
    """
    Selects the first Nation on Nation selection screen.
    """

    app_window = get_app_window()
    banner_position = app_window.banner_position
    pyautogui.click(banner_position)


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
    config.move_log(simulation_round)
