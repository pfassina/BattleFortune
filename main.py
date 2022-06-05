from src import battlefortune as bf
from src.config import SimConfig


def main(config: SimConfig):

    # gui.initialize()
    bf.start(config)


if __name__ == '__main__':
    from debug_request import config
    main(config)