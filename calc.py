import ast
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dict


def wincalc(winlog):

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

    df = pd.DataFrame(battlelog)
    df.columns = ['Turn', 'Phase', 'Army', 'Count', 'Unit']
    df['Army'] = df['Army'].replace(dict.nations())


    return df
