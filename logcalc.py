import pandas as pd
import dict


def wincalc(winlog):
    '''
    Parses a list of WinLogs and calculates the ratio of winnings per Nation.
    Takes as input a list of WinLogs.
    Returns a DataFrame with the Win Counts per Nation.
    '''

    # Decode Nation IDs
    df = pd.DataFrame(winlog)
    df.columns = ['Turn', 'Winner']
    df['Nation'] = df['Winner'].replace(dict.nations())

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
    df.columns = ['Turn', 'Phase', 'Army', 'Count', 'Unit']
    df['Army'] = df['Army'].replace(dict.nations())

    return df
