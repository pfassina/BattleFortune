import pandas as pd

from src import decode, globals


def wins():
    """
    Parses a list of WinLogs and calculates the ratio of winnings per Nation.
    :return: DataFrame with Win Counts per Nation.
    """

    # Decode Nation IDs
    df = pd.DataFrame(globals.LOGS['winners'])
    df['Nation'] = df['Nation'].apply(lambda x: decode.nation(x))

    # Prepare Data for Display
    df = df['Nation'].value_counts().to_frame('Wins')
    df = df.reset_index().rename(columns={'index': 'Nation'})

    globals.WIN_COUNTS = df


def pivot_battle_log():
    """
    Prepares battle log for manipulation.
    :return: Battle Log DataFrame
    """

    c = ['Army', 'Unit', 'Phase']
    df = pd.DataFrame(globals.LOGS['battles'])
    df = df.pivot_table(values='Count', index='Turn', columns=c, aggfunc='sum')
    return df


def unit_losses(df, army):
    """
    Calculates Unit losses by army.
    :param df: Battle Log DataFrame
    :param army: One of the Nations participating in the battle
    :return: DataFrame with calculated unit losses
    """

    # filter by army
    army_df = df[army].copy()
    army_units = army_df.columns.get_level_values('Unit').unique()

    # calculate unit loss per round
    army_results = []
    for item in army_units:
        temp = army_df[item].copy()
        temp[item] = temp.get('after', 0) - temp.get('before', 0)
        # temp.columns.rename(item)
        army_results.append(temp[item])

    # assemble army DataFrame
    army_losses = pd.DataFrame({'Turn': range(1, globals.SIMULATIONS + 1)})
    for item in army_results:
        army_losses = army_losses.join(item, on='Turn')

    # reset index and fill na with zero
    army_losses.set_index('Turn', inplace=True)
    army_losses = army_losses.fillna(0)

    return army_losses


def army_cost(df, attribute):
    """
    Calculates total resource cost per round of simulation.
    :param df: Army Losses DataFrame
    :param attribute: Either "gold" or "resources"
    :return: DataFrame with total resource cost per round
    """

    # get units from army DataFrame
    units = df.columns.get_level_values(0).unique()

    # apply attribute cost to each unit
    ac = df.copy()
    for item in units:
        ac[item] = ac[item].apply(lambda x: x * decode.unit(item, attribute))

    # calculate each round cost by adding up unit costs
    ac[attribute] = ac.sum(axis=1)
    ac = ac[attribute]

    return ac


def summary():
    """
    Converts battle log into DataFrames
    :return: dictionary with attacker and defender DataFrames
    """

    nations = globals.LOGS['nations']

    df = pivot_battle_log()
    globals.ATTACKER_DF = unit_losses(df, nations['defender'])
    globals.DEFENDER_DF = unit_losses(df, nations['attacker'])


def results():

    wins()
    summary()
