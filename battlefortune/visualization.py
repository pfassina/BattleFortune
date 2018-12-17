import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logcalc
from decode import nation


def load_battlelog(battlelog, nations):

    df = logcalc.pivot_battlelog(battlelog)
    attacker = logcalc.calculate_unit_losses(df, nations['attacker'])
    defender = logcalc.calculate_unit_losses(df, nations['defender'])

    dataframes = {
        'attacker': attacker,
        'defender': defender
    }

    return dataframes


def distribution_charts(dataframes, nations):

    attacker = dataframes['attacker']
    defender = dataframes['defender']

    gcost = logcalc.calculate_army_cost(attacker, 'gcost')
    attacker = attacker.join(gcost)

    gcost = logcalc.calculate_army_cost(defender, 'gcost')
    defender = defender.join(gcost)

    atk_name = nation(nations['attacker'])
    def_name = nation(nations['defender'])

    a = pd.Series(attacker['gcost'], name=atk_name)
    d = pd.Series(defender['gcost'], name=def_name)
    df = pd.concat([a, d], axis=1)

    df[atk_name + " ROI"] = df[def_name] - df[atk_name]
    df[def_name + " ROI"] = df[atk_name] - df[def_name]

    try:
        plt.subplot(211)
        sns.distplot(df[atk_name + " ROI"])

        plt.subplot(212)
        sns.distplot(df[def_name + " ROI"])

        # plt.subplot(223)
        sns.jointplot(x=atk_name, y=def_name, data=df, kind="kde")
    except ArithmeticError:
        pass

    plt.show()
