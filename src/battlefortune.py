from src import calculate, read, visualize, utility, run
from src.config import SimConfig


def start(config: SimConfig) -> None:
    """
    Runs BattleFortune, simulate battles, and return results.
    """

    # PREPARE
    utility.clone_game_files(config.game_path, config.simulations)

    # SIMULATE
    rounds = run.simulation(config)

    # LOG
    logs = read.combine_logs(config, rounds)

    # CALCULATE
    results = calculate.results(logs)

    # DISPLAY
    visualize.charts(results)

    # CLEAN
    utility.remove_cloned_files(config.game_path, config.simulations)