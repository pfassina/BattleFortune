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
