import os

import yaml

from src import calculate, read, visualize, utility, globals, run


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


def setup(dom_path, game_path):
    """
    Setups config.yaml file with file paths.
    :param dom_path: OS path to dominions executable file
    :param game_path: OS path to game folder
    """

    path_dict = {
        'dom_path': dom_path,
        'game_path': game_path
    }

    with open('./data/config.yaml', 'w') as outfile:
        yaml.dump(path_dict, stream=outfile)

    if not os.path.exists('img/'):
        os.makedirs('img/')


def startup(inputs):

    globals.init()

    setup(dom_path= inputs['dp'], game_path=inputs['gp'])

    globals.DOM_PATH = inputs['dp']
    globals.GAME_PATH = os.path.join(inputs['gp'], inputs['gn'])
    globals.GAME_NAME = inputs['gn']
    globals.PROVINCE = int(inputs['pn'])
    globals.SIMULATIONS = int(inputs['sr'])

    battlefortune()
