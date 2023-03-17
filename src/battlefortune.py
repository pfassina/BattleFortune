from src import calculate, read, run, visualize
from src.config import CONFIG


def start() -> None:
    """
    Runs BattleFortune, simulate battles, and return results.
    """

    # PREPARE
    CONFIG.clone_game_files()

    # SIMULATE
    turns = run.simulation()

    # LOG
    logs = read.combine_logs(turns)

    # CALCULATE
    results = calculate.results(logs)

    # DISPLAY
    visualize.charts(results)

    # CLEAN
    CONFIG.remove_cloned_files()
