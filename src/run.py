import os
import signal
import subprocess
import threading
import time

from tqdm import tqdm

from src import process, globals


def run_command(game, host_game):
    if host_game:
        return ['./dom5_mac', '--simpgui', '--nosteam', '-waxscog', '-T', game]
    else:
        return ['./dom5_mac', '--simpgui', '--nosteam', "'--res 960 720'", '-waxscod', game]


def run_dominions(game, host_game=False):
    """
    Run command for Dominions
    :param game: game name
    :param host_game: True to host battle
    :return: run process
    """

    if host_game:
        dom_instance = subprocess.Popen(run_command(game, host_game), cwd=globals.DOM_PATH)
    else:
        with open(os.path.join(globals.DOM_PATH, 'log.txt'), 'w') as log:
            dom_instance = subprocess.Popen(run_command(game, host_game), cwd=globals.DOM_PATH, stdout=log)

    return dom_instance.pid


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
            time.sleep(1)
            done = True
            break

    return done


def host(simulation_round):
    """
    host battle for a single round
    :param simulation_round: simulation round
    :return: True if successful
    """

    simulation_name = f'{globals.GAME_NAME}_{str(simulation_round)}'
    simulation_path = f'{globals.GAME_PATH}_{str(simulation_round)}/'

    start_time = os.path.getmtime(simulation_path + 'ftherlnd')
    process_id = run_dominions(game=simulation_name, host_game=True)
    success = validate_host(simulation_path, start_time=start_time)

    if success:
        globals.VALID_ROUNDS.append(simulation_round)

    else:
        globals.FAILED_ROUNDS.append(simulation_round)

    os.kill(process_id, signal.SIGTERM)


def batch_host():
    """"
    Host games concurrently based on the number of threads.
    """

    threads = []
    for round in range(globals.SIMULATIONS):

        t = threading.Thread(target=host, kwargs={'simulation_round': round + 1})
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()


def batch_process():
    """
    Clicks through a Dominions game to generate log
    :return: True if successful
    """

    for r in tqdm(globals.VALID_ROUNDS):
        pid = run_dominions(f'{globals.GAME_NAME}_{str(r)}')
        process.rounds(simulation_round=r, process_id=pid)


def simulation():
    """
    Runs X numbers of Simulation Rounds.
    :return: list of simulation rounds that successfully generated logs
    """

    # Host simulations
    batch_host()

    # Process hosted games
    batch_process()
