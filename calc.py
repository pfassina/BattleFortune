import ast
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dict


def logtodict():

    with open('./output/winlog.txt', 'r') as f:
        wl = [line.strip() for line in f]
    for i in range(len(wl)):
        wl[i] = ast.literal_eval(wl[i])

    with open('./output/battlelog.txt', 'r') as f:
        blfile = [line.strip() for line in f]
    for i in range(len(blfile)):
        blfile[i] = ast.literal_eval(blfile[i])

    bl = []
    for i in range(len(blfile)):
        for j in range(len(blfile[i])):
            bl.append(blfile[i][j])

    return wl, bl


# wl = logtodict()[0]
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


bl = logtodict()[1]
def battlecalc(battlelog):

    df = pd.DataFrame(battlelog)
    df.columns = ['Turn', 'Phase', 'Army', 'Count', 'Unit']
    df['Army'] = df['Army'].replace(dict.nations())


    return df

print(battlecalc(bl)['Turn'])
