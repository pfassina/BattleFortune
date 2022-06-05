from src import battlefortune as bf
from src.config import SimConfig


def main(config: SimConfig):

    # gui.initialize()
    bf.start(config)


if __name__ == '__main__':
    dp = '/Users/pfass/Library/Application Support/Steam/steamapps/common/Dominions5'
    gp = '/Users/pfass/.dominions5/savedgames'
    gn = 'test'
    sr = 10
    pn = 6
    config = SimConfig(dominions_path=dp,
                       game_dir=gp,
                       game_name=gn,
                       simulations=sr,
                       province=pn)
    main(config)