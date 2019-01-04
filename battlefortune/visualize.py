import calculate
from decode import nation
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# set visualization palette
sns.set(palette="Set3", style="white")


def load_battle_log(battle_log, nations, rounds):
    """
    Converts battle log into DataFrames
    :param rounds: total number of rounds being simulated
    :param battle_log: list of battle logs dictionaries
    :param nations: list of nations
    :return: dictionary with attacker and defender DataFrames
    """

    df = calculate.pivot_battlelog(battle_log)
    defender = calculate.unit_losses(df, nations['defender'], rounds)
    attacker = calculate.unit_losses(df, nations['attacker'], rounds)

    dataframes = {
        'attacker': attacker,
        'defender': defender
    }

    return dataframes


def win_score(win_log):
    """
    Generates Win Score bar plot
    :param win_log: win log file
    :return: win score bar plot
    """

    df = calculate.wins(win_log)
    plt.figure(1)
    sns.barplot(x='Nation', y='Wins', data=df)


def unit_deaths(dataframes):
    """
    Generates unit losses bar plot
    :param dataframes: dictionary with attacker and defender DataFrames
    :return: unit losses bar plot
    """

    attacker = dataframes['attacker']
    defender = dataframes['defender']

    try:
        plt.figure(2)

        plt.subplot(211)
        sns.violinplot(data=attacker, scale="width")

        plt.subplot(212)
        sns.violinplot(data=defender, scale="width")

    except ArithmeticError:
        pass


def army_roi(dataframes, nations):
    """
    Generates the Army ROI distribution plots
    :param dataframes: dictionary with attacker and defender DataFrames
    :param nations: list of nations
    :return:
    """

    attacker = dataframes['attacker']
    defender = dataframes['defender']

    gcost = calculate.army_cost(attacker, 'gcost')
    attacker = attacker.join(gcost)

    gcost = calculate.army_cost(defender, 'gcost')
    defender = defender.join(gcost)

    atk_name = nation(nations['attacker'])
    def_name = nation(nations['defender'])

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


def visualize(nations, win_log, battle_log, rounds):
    """
    Calculate and Visualize battle results
    :param rounds: Total number of rounds being simulated
    :param nations: Nations participating in the battle
    :param win_log: list of win logs
    :param battle_log: list of battle logs
    :return: plot visualizations
    """

    df = load_battle_log(battle_log, nations, rounds)
    win_score(win_log)
    army_roi(df, nations)
    unit_deaths(df)

    plt.show()
