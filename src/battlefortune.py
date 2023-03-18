import logging
import os
import shutil

from src import calculate, read, run, visualize
from src.config import CONFIG


def start() -> None:
    """
    Runs BattleFortune, simulate battles, and return results.
    """

    # PREPARE
    clone_game_files()

    # SIMULATE
    turns = run.simulation()

    # LOG
    logs = read.combine_logs(turns)

    # CALCULATE
    results = calculate.results(logs)

    # DISPLAY
    visualize.charts(results)

    # CLEAN
    remove_cloned_files()


def clone_game_files() -> None:
    logging.info("cloning game files")
    for turn in CONFIG.data.simulation_turns:
        if os.path.exists(CONFIG.data.simulation_path(turn)):
            logging.info("previous simulation files detected. removing old files.")
            shutil.rmtree(CONFIG.data.simulation_path(turn))
        logging.info(f"creating files for simulation {turn}")
        shutil.copytree(CONFIG.data.game_path, CONFIG.data.simulation_path(turn))


def remove_cloned_files() -> None:
    for turn in CONFIG.data.simulation_turns:
        shutil.rmtree(CONFIG.data.simulation_path(turn))
