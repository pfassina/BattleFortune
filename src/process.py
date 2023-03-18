import logging
import os
import shutil
from dataclasses import dataclass
from time import sleep

import keyboard
import pyautogui

from src.config import CONFIG
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
    platform: PlatformProtocol
    simulation_round: int
    process_id: int

    @property
    def log_path(self) -> str:
        return os.path.join(CONFIG.data.dominions_path, "log.txt")

    @property
    def dx(self) -> int:
        return CONFIG.data.banner_x

    @property
    def dy(self) -> int:
        return CONFIG.data.banner_y

    @property
    def province(self) -> str:
        return str(CONFIG.data.province)

    def get_app_window(self) -> AppWindow:
        logging.info("looking for dom5 window")
        x, y = self.platform.get_app_window()
        logging.info(f"dom5 window found: {(x, y)}")
        return AppWindow(x, y)

    def select_nation(self) -> None:
        logging.info("selecting nation")
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
        logging.info("click succesful")

    def check_log(self, text: str) -> bool:
        if not os.path.exists(self.log_path):
            return False

        logging.info("log found")
        with open(self.log_path, "r") as log:
            blurb = log.read()

        return blurb.rfind(text) != -1

    def go_to_province(self) -> None:
        logging.info("checking battle results")
        keyboard.press_and_release("esc")  # exit messages
        keyboard.press_and_release("g")  # go to screen
        keyboard.write(self.province)  # select province
        keyboard.press_and_release("enter")  # confirm
        keyboard.press_and_release("c")  # view results
        keyboard.press_and_release("esc")  # back to map
        keyboard.press_and_release("d")  # try to add PD
        while not self.check_log("getfatherland"):
            sleep(0.1)

    def move_log(self, turn: int, save_log: bool = False) -> None:
        src = os.path.join(CONFIG.data.dominions_path, "log.txt")
        dst = os.path.join(CONFIG.data.simulation_path(turn), "log.txt")
        shutil.copy(src, dst)

        if save_log:
            copy = os.path.join("logs", f"{CONFIG.data.game_name}_{turn}.log")
            shutil.copy(src, copy)

    def process_turn(self) -> None:
        # select first nation
        self.select_nation()

        # check battle report
        self.go_to_province()

        # terminate process
        self.platform.kill_process(self.process_id)

        # move log to round folder
        self.move_log(self.simulation_round)
