import pandas as pd
from decode import nation
import yaml


def wincalc(winlog):
    '''
    Parses a list of WinLogs and calculates the ratio of winnings per Nation.
    Takes as input a list of WinLogs.
    Returns a DataFrame with the Win Counts per Nation.
    '''

    # Decode Nation IDs
    df = pd.DataFrame(winlog)
    df['Nation'] = df['Nation'].apply(lambda x: nation(x))

    # Prepare Data for Display
    df = df['Nation'].value_counts().to_frame('Wins')
    df = df.reset_index().rename(columns={'index': 'Nation'})
    df = pd.pivot_table(df, values='Wins', columns='Nation')

    return df


def battlecalc(battlelog):
    '''
    Parses a list of BattleLogs and calculates the results.
    Takes as input a list of  BattleLogs.
    Returns a DataFrame with the Battle Results per Nation.
    '''

    df = pd.DataFrame(battlelog)
    df['Army'] = df['Army'].apply(lambda x: nation(x))

    return df


def pivot_battlelog(battlelog):
    '''
    Prepares battlelog for manipulation.
    Takes as input a disctionary-like battlelog.
    Outputs a pandas DataFrame.
    '''

    c = ['Army', 'Unit', 'Phase']
    df = pd.DataFrame(battlelog)
    df = df.pivot_table(values='Count', index='Turn', columns=c, aggfunc='sum')

    return df


def calculate_unit_losses(df, army):
    '''
    Calculates Unit losses by army.
    Takes as input a prepared battlelog DataFrame.
    Returns an army DataFrame with losses per unit
    '''

    # filter by army
    army_df = df[army].copy()
    army_units = army_df.columns.get_level_values('Unit').unique()

    # calculate unit loss per round
    army_results = []
    for item in army_units:
        temp = army_df[item].copy()
        temp[item] = temp['after'] - temp['before']
        # temp.columns.rename(item)
        army_results.append(temp[item])

    # assemple army dataframe
    army_losses = pd.DataFrame({'Turn': range(1, 101)})
    for item in army_results:
        army_losses = army_losses.join(item, on='Turn')

    # reset index and fill na with zero
    army_losses.set_index('Turn', inplace=True)
    army_losses = army_losses.fillna(0)

    return army_losses


def get_unit_cost(name, attribute):
    '''
    Searches Unit by Name and Returns Attribute Cost.
    Attribute can either be 'gold' or 'resources'.
    '''

    # load data from unit database
    units = yaml.load(open('./data/units.yaml', 'r'))

    # search unit by name return attribute cost
    for key in units:
        if units[key]['name'] == name:
            cost = units[key][attribute]

    return cost


def calculate_army_cost(df, attribute):
    '''
    Takes Army Losses DataFrame.
    Returns total resource cost per round of simulation.
    Accepets 'gold' or 'resources' as attribute cost.
    '''

    # get units from army DataFrame
    units = df.columns.get_level_values(0).unique()

    # apply attribute cost to each unit
    ac = df.copy()
    for item in units:
        ac[item] = ac[item].apply(lambda x: x * get_unit_cost(item, attribute))

    # calculate each round cost by adding up unit costs
    ac[attribute] = ac.sum(axis=1)
    ac = ac[attribute]

    return ac
