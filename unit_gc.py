import pandas as pd


def trim_unit_table(path='./data/units.csv'):

    df = pd.read_csv(path, sep='\t')
    u = ['basecost', 'rt', 'holy']
    c = ['leader', 'inspirational', 'sailingshipsize']
    r = ['rand1', 'rand2', 'rand3', 'rand4', 'rand5', 'rand6']
    m = ['F', 'A', 'W', 'E', 'S', 'D', 'N', 'B']
    p = ['researchbonus', 'fixforgebonus']
    h = ['H']
    s = ['spy', 'assassin', 'seduce', 'succubus']
    x = ['stealthy', 'autohealer', 'autodishealer', 'mounted']

    col = u + c + r + m + p + h + s + x

    df = df[col]

    return df


def leader_cost(leader, inspirational, sailingshipsize):

    lc = 0
    leadership = {
        0:	10,
        10:	15,
        20: 20,
        30: 55,
        40: 30,
        60: 30,
        80: 60,
        100: 80,
        120: 100,
        160: 150
    }

    lc += leadership[leader]
    lc += inspirational * 10
    if sailingshipsize > 0:
        lc += lc * 0.5

    return lc


def priest_cost(H):

    pc = 0
    holy = {
        1: 20,
        2: 40,
        3: 80,
        4: 140
    }

    if H is not None:
        pc += holy[H]

    return pc


def spy_cost(spy, assassin, seduce, succubus):

    sc = 0
    if spy > 0:
        sc += 40
    if assassin > 0:
        sc += 40
    if seduce > 0:
        sc += 60
    if succubus > 0:
        sc += 60

    return sc


def special_cost(stealthy, autohealer, autodishealer, mounted):

    xc = 0
    if stealthy > 0:
        xc += 5
    if autohealer > 0:
        xc += 50
    if autodishealer > 0:
        xc += 20
    if mounted > 0:
        xc += 10

    return xc


def assemble_costs(lc, mc, pc, sc, xc):

    cost = {
        'lc': lc,
        'mc': mc,
        'pc': pc,
        'sc': sc,
        'xc': xc
    }

    return cost


def dom_round(cost, needed=True):

    if needed:
        cost = int(cost / 5) * 5

    elif cost >= 30:
        cost = int(cost / 5) * 5

    else:
        cost = int(cost)

    return cost


def gold_cost(basecost, costs, rt=None, holy=None):

    if basecost > 1000:

        lc = costs['lc']
        mc = costs['mc'] / 2
        pc = costs['pc'] / 2
        sc = costs['sc'] / 2
        xc = costs['xc']

        gc = lc + mc + pc + sc + xc
        gc += (basecost - 10000)

        if rt == 2:
            gc = gc * 0.9
        if holy > 0:
            gc = gc * 1.3

        print(gc)
        gc = dom_round(gc, needed=True)

    else:
        gc = basecost
        gc = dom_round(gc, needed=False)

    return gc


def paths_cost(mpaths, rpaths, researchbonus, fixforgebonus):

    mc = 0

    mc += mpaths
    mc += rpaths

    if researchbonus > 0:
        mc += researchbonus * 5
    elif researchbonus < 0:
        mc -= 5

    if fixforgebonus > 0:
        mc += mc * fixforgebonus / 100

    return mc


def randompaths(rpaths):

    masks = {
        128: 'F',
        256: 'A',
        512: 'W',
        1024: 'E',
        2048: 'S',
        4096: 'D',
        8192: 'N',
        16384: 'B',
        32768: 'H'
    }

    randompaths = []
    for i in range(4):
        paths = rpaths[i]['mask' + str(i + 1)]
        levels = rpaths[i]['link' + str(i + 1)]
        chance = rpaths[i]['rand' + str(i + 1)]
        repeat = rpaths[i]['nbr' + str(i + 1)]
        rp = {
            'paths': masks[paths],
            'levels': levels,
            'chance': chance
        }
        for i in range(repeat):
            randompaths.append(rp)

    return randompaths


rpaths = [
    {'rand1': None, 'nbr1': 1, 'link1': None, 'mask1': 128},
    {'rand2': None, 'nbr2': 1, 'link2': None, 'mask2': 256},
    {'rand3': None, 'nbr3': 1, 'link3': None, 'mask3': 512},
    {'rand4': None, 'nbr4': 1, 'link4': None, 'mask4': 1024}
]
