import os
import signal
from dataclasses import dataclass
from time import sleep

import keyboard
import pyautogui
import Quartz

from src.config import SimConfig


@dataclass
class AppWindow:
    x: int
    y: int

    def banner_position(self, dx: int, dy: int) -> tuple[int, int]:
        banner_x = self.x + dx
        banner_y = self.y + dy
        return (banner_x, banner_y)


@dataclass
class TurnRobot:
    config: SimConfig
    simulation_round: int
    process_id: int

    @property
    def log_path(self) -> str:
        return os.path.join(self.config.dominions_path, "log.txt")

    @property
    def dx(self) -> int:
        return self.config.banner_x

    @property
    def dy(self) -> int:
        return self.config.banner_y

    @property
    def province(self) -> str:
        return str(self.config.province)

    def wait_screen_load(self) -> None:
        while not os.path.exists(self.log_path):
            continue

        sleep(1)

        with open(self.log_path, "r") as log:
            load_complete = -1
            while load_complete == -1:
                blurb = log.read()
                load_complete = blurb.rfind("playturn: autohost")

    def get_app_window(self) -> AppWindow:
        apps = Quartz.CGWindowListCopyWindowInfo(  # type: ignore
            Quartz.kCGWindowListOptionOnScreenOnly  # type: ignore
            & Quartz.kCGWindowListExcludeDesktopElements,  # type: ignore
            Quartz.kCGNullWindowID,  # type: ignore
        )

        dom_5_apps = (a for a in apps if a.get("kCGWindowOwnerName") == "dom5_mac")
        dom_5 = next(a for a in dom_5_apps if a.get("kCGWindowIsOnscreen") == 1)
        window = dom_5.get("kCGWindowBounds")

        return AppWindow(window["X"], window["Y"])

    def select_nation(self) -> None:
        app_window = self.get_app_window()
        banner_position = app_window.banner_position(self.dx, self.dy)
        pyautogui.click(banner_position)

    def go_to_province(self) -> None:
        keyboard.press_and_release("esc")  # exit messages
        keyboard.press_and_release("g")  # go to screen
        keyboard.write(self.province)  # select province
        keyboard.press_and_release("enter")  # confirm
        keyboard.press_and_release("c")  # view results
        keyboard.press_and_release("esc")  # back to map
        keyboard.press_and_release("d")  # try to add PD

    def process_turn(self) -> None:
        self.wait_screen_load()

        # select first nation
        self.select_nation()

        # check battle report
        self.go_to_province()

        # terminate process
        os.kill(self.process_id, signal.SIGTERM)

        # move log to round folder
        self.config.move_log(self.simulation_round)
