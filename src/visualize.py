import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src import calculate, decode, globals

# set visualization palette
sns.set(palette="Set3", style="white")


def win_score():
    """
    Generates Win Score bar plot
    :return: win score bar plot
    """

    df = globals.WIN_COUNTS
    plt.figure(1)
    sns.barplot(x='Nation', y='Wins', data=df)


def army_roi():
    """
    Generates the Army ROI distribution plots
    :return:
    """

    attacker = globals.ATTACKER_DF
    defender = globals.DEFENDER_DF

    gcost = calculate.army_cost(attacker, 'gcost')
    attacker = attacker.join(gcost)

    gcost = calculate.army_cost(defender, 'gcost')
    defender = defender.join(gcost)

    nations = globals.LOGS['nations']
    atk_name = decode.nation(nations['attacker'])
    def_name = decode.nation(nations['defender'])

    a = pd.Series(attacker['gcost'], name=atk_name)
    d = pd.Series(defender['gcost'], name=def_name)
    df = pd.concat([a, d], axis=1)

    df[atk_name + ' ROI'] = df[def_name] - df[atk_name]
    df[def_name + ' ROI'] = df[atk_name] - df[def_name]

    try:
        plt.figure(3)
        plt.subplot(211)
        sns.distplot(df[atk_name + ' ROI'])

        plt.subplot(212)
        sns.distplot(df[def_name + ' ROI'])

        sns.jointplot(x=atk_name, y=def_name, data=df, kind="kde")

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
        sns.violinplot(data=attacker, scale="width")

        plt.subplot(212)
        sns.violinplot(data=defender, scale="width")

    except ArithmeticError:
        pass


def charts():
    """
    Visualize battle results
    :return: plot visualizations
    """

    win_score()
    army_roi()
    unit_deaths()

    plt.show()
