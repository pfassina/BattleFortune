import os
import signal
from dataclasses import dataclass
from time import sleep

import keyboard
import pyautogui

from src.config import SimConfig
from src.platform import PlatformProtocol


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
    platform: PlatformProtocol
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

    def get_app_window(self) -> AppWindow:
        x, y = self.platform.get_app_window()
        return AppWindow(x, y)

    def select_nation(self) -> None:
        while not self.check_log("playturn: autohost"):
            sleep(0.1)

        app_window = self.get_app_window()
        banner_position = app_window.banner_position(self.dx, self.dy)

        click_counter = 0
        while not self.check_log("Viewmessages"):
            pyautogui.click(banner_position)
            sleep(0.1)
            click_counter += 1
            if click_counter > 50:
                raise TimeoutError

    def check_log(self, text: str) -> bool:
        if not os.path.exists(self.log_path):
            return False

        with open(self.log_path, "r") as log:
            blurb = log.read()
        return blurb.rfind(text) != -1

    def go_to_province(self) -> None:
        keyboard.press_and_release("esc")  # exit messages
        keyboard.press_and_release("g")  # go to screen
        keyboard.write(self.province)  # select province
        keyboard.press_and_release("enter")  # confirm
        keyboard.press_and_release("c")  # view results
        keyboard.press_and_release("esc")  # back to map
        keyboard.press_and_release("d")  # try to add PD
        sleep(0.1)

    def process_turn(self) -> None:
        # select first nation
        self.select_nation()

        # check battle report
        self.go_to_province()

        # terminate process
        os.kill(self.process_id, signal.SIGTERM)

        # move log to round folder
        self.config.move_log(self.simulation_round)
