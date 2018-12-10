import pandas as pd
from decode import nation

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

    df = pd.DataFrame(battlelog)
    df = df.pivot_table(values='Count', index='Turn', columns=['Army', 'Unit', 'Phase'], aggfunc='sum')

    return df



def calculate_losses(df, army):
    '''
    Calculates Unit losses by army.
    Takes as input a prepared battlelog DataFrame.
    Returns an army DataFrame with losses per unit
    '''

    # filter by army
    army_df = df[army].copy()
    army_units = army_df.columns.get_level_values('Unit').unique()

    # calculate final unit loss
    army_results = []
    for item in army_units:
        temp = army_df[item].copy()
        temp[item] = temp['after'] - temp['before']
        # temp.columns.rename(item)
        army_results.append(temp[item])

    # create final army dataframe
    army_losses = pd.DataFrame({'Turn': range(1, 101)})
    for item in army_results:
        army_losses = army_losses.join(item, on='Turn')

    army_losses.set_index('Turn', inplace=True)
    army_losses = army_losses.fillna(0)

    return army_losses
