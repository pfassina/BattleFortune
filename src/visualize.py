import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src import calculate, decode, globals

# set visualization palette
sns.set(palette="Set3", style="white", rc={'figure.figsize': (12.8, 9.6), 'figure.dpi': 72})


def win_score():
    """
    Generates Win Score bar plot
    :return: win score bar plot
    """

    df = globals.WIN_COUNTS
    plt.figure(1)
    plot = sns.barplot(x='Nation', y='Wins', data=df).get_figure()
    plot.savefig('img/winscore.png')


def army_roi(cost_type):
    """
    Generates the Army ROI distribution plots
    :return:
    """

    attacker = globals.ATTACKER_DF
    defender = globals.DEFENDER_DF

    cost = calculate.army_cost(attacker, cost_type)
    attacker = attacker.join(cost)

    cost = calculate.army_cost(defender, cost_type)
    defender = defender.join(cost)

    nations = globals.LOGS['nations']
    atk_name = decode.nation(nations['attacker'])
    def_name = decode.nation(nations['defender'])

    a = pd.Series(attacker[cost_type], name=atk_name)
    d = pd.Series(defender[cost_type], name=def_name)
    df = pd.concat([a, d], axis=1)

    df[atk_name + ' ROI'] = df[def_name] - df[atk_name]
    df[def_name + ' ROI'] = df[atk_name] - df[def_name]

    try:
        plt.figure(3)
        plt.subplot(211)
        sns.distplot(df[atk_name + ' ROI']).get_figure()

        plt.subplot(212)
        plot = sns.distplot(df[def_name + ' ROI']).get_figure()
        plot.savefig('img/defender_roi.png')

        plot = sns.jointplot(x=atk_name, y=def_name, data=df, kind="kde")
        plot.savefig('img/army_roi.png')

    except ArithmeticError:
        pass


def unit_deaths():
    """
    Generates unit losses bar plot
    :return: unit losses bar plot
    """

    attacker = globals.ATTACKER_DF
    defender = globals.DEFENDER_DF

    try:
        plt.figure(2)

        plt.subplot(211)
        plot = sns.violinplot(data=attacker, scale="width").get_figure()

        plt.subplot(212)
        plot = sns.violinplot(data=defender, scale="width").get_figure()
        plot.savefig('img/defender_unit_deaths.png')

    except ArithmeticError:
        pass


def charts():
    """
    Visualize battle results
    :return: plot visualizations
    """

    win_score()
    army_roi(cost_type='gcost')
    unit_deaths()

    plt.show()
