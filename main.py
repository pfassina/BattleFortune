from src import battlefortune


if __name__ == '__main__':

    dp = input('dominions 5 executable path: ')
    gp = input('saved games path: ')

    battlefortune.setup(dom_path=dp, game_path=gp)

    gn = input('game name: ')
    sr = input('simulation rounds: ')
    pn = input('province number: ')

    battlefortune.startup(game=gn, simulations=sr, province=pn)
    battlefortune.battlefortune()
