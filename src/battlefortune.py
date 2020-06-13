import yaml

from src import calculate, read, visualize, utility, globals, run


def setup(dom_path, game_path):
    """
    Setups config.yaml file with file paths.
    :param dom_path: OS path to dominions executable file
    :param game_path: OS path to game folder
    """

    path_dict = {
        dom_path: None,
        game_path: None
    }

    with open('./data/config.yaml', 'w') as outfile:
        yaml.dump(path_dict, stream=outfile)


def startup(game, simulations, province):

    globals.init()

    with open('./data/config.yaml', 'r') as file:
        paths = yaml.load(file, Loader=yaml.Loader)

    globals.DOM_PATH = paths['dom_path']
    globals.GAME_PATH = paths['game_path']

    globals.SIMULATIONS = simulations
    globals.GAME_NAME = game
    globals.PROVINCE = province


def battlefortune():
    """
    Runs BattleFortune, simulate battles, and return results.
    """

    # PREPARE
    utility.clone_game_files()

    # SIMULATE
    run.simulation()

    # LOG
    read.combine_logs()

    # CALCULATE
    calculate.results()

    # DISPLAY
    visualize.charts()

    # CLEAN
    utility.remove_cloned_files()
