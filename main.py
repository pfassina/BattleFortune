from src import battlefortune


if __name__ == '__main__':

    kwargs = {
        'game': 'test',
        'simulations': 5,
        'province': 6,
    }

    battlefortune.startup(**kwargs)
    battlefortune.battlefortune()
