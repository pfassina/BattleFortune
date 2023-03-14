from src import calculate, read, visualize, run
from src.config import SimConfig


def start(config: SimConfig) -> None:
    """
    Runs BattleFortune, simulate battles, and return results.
    """

    # PREPARE
    config.clone_game_files()

    # SIMULATE
    turns = run.simulation(config)

    # LOG
    logs = read.combine_logs(config, turns)

    # CALCULATE
    results = calculate.results(logs)

    # DISPLAY
    visualize.charts(results)

    # CLEAN
    config.remove_cloned_files()
