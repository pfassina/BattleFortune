import os
import signal
import subprocess
import threading
import time

from tqdm import tqdm

from src import process
from src.config import SimConfig

VALID_ROUNDS: list[int] = []


def run_command(game_name: str, host_game: bool) -> list[str]:
    command = ["./dom5_mac", "--simpgui", "--nosteam"]

    if host_game:
        return command + ["-waxscog", "-T", game_name]

    return command + ["--res", "960", "720", "-waxscod", game_name]


def run_dominions(dominions_path: str, game_name: str, host_game: bool) -> int:
    """
    Run command for Dominions
    :param game: game name
    :param host_game: True to host battle
    :return: run process
    """

    cmd = run_command(game_name, host_game)
    if host_game:
        return subprocess.Popen(cmd, cwd=dominions_path).pid

    log_path = os.path.join(dominions_path, "log.txt")
    with open(log_path, "w") as log:
        return subprocess.Popen(cmd, cwd=dominions_path, stdout=log).pid


def wait_for_host(path: str, start_time: float) -> bool:
    """
    Waits Dominions to Host battle.
    :param path: dominions game path
    :param start_time: Time when ftherlnd was last updated
    :return: True if ftherlnd was updated
    """

    # Loop until host is finished
    while os.path.getmtime(path) == start_time:
        time.sleep(1)

    return True


def host(config: SimConfig, simulation: int) -> None:
    """
    host battle for a single round
    :param simulation_round: simulation round
    :return: True if successful
    """

    game_name = f"{config.game_name}_{simulation}"
    game_path = f"{config.game_path}_{simulation}"
    ftherland_path = os.path.join(game_path, "ftherlnd")

    start_time = os.path.getmtime(ftherland_path)
    process_id = run_dominions(config.dominions_path, game_name, host_game=True)

    if wait_for_host(ftherland_path, start_time):
        VALID_ROUNDS.append(simulation)

    os.kill(process_id, signal.SIGTERM)


def batch_host(config: SimConfig) -> None:
    """ "
    Host games concurrently based on the number of threads.
    """

    threads = []
    for simulation in range(config.simulations):
        simulation_args = {"config": config, "simulation": simulation + 1}

        t = threading.Thread(target=host, kwargs=simulation_args)
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def batch_process(config: SimConfig) -> None:
    """
    Clicks through a Dominions game to generate log
    :return: True if successful
    """

    for r in tqdm(VALID_ROUNDS):
        sim_path = f"{config.game_name}_{r}"
        pid = run_dominions(config.dominions_path, sim_path, False)
        process.rounds(config, simulation_round=r, process_id=pid)


def simulation(config: SimConfig) -> list[int]:
    """
    Runs X numbers of Simulation Rounds.
    :return: list of simulation rounds that successfully generated logs
    """

    # Host simulations
    batch_host(config)

    # Process hosted games
    batch_process(config)

    return VALID_ROUNDS
