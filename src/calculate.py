from dataclasses import dataclass
import pandas as pd

from src.read import ParsedLogs, Phase
from src.decode import Nation


@dataclass
class Results:
    attacker: Nation
    defender: Nation
    win_score: pd.Series
    unit_losses: pd.DataFrame

    @property
    def army_cost(self) -> pd.DataFrame:
        return self.unit_losses.groupby(level=[0, 1]).sum()  # type: ignore


def wins(logs: ParsedLogs):
    """
    Parses a list of WinLogs and calculates the ratio of winnings per Nation.
    :return: DataFrame with Win Counts per Nation.
    """

    df = pd.DataFrame.from_dict(logs.winners, orient='index').sum(axis=1)
    return df


def unit_results(logs: ParsedLogs, nation: Nation) -> pd.DataFrame:
    battles = logs.battles[nation]
    results = {unit: battles[unit] for unit in logs.units(nation)}
    return pd.DataFrame.from_dict(results, orient='index')


def unit_dataframe(results: pd.DataFrame) -> pd.DataFrame:
    b = results.apply(lambda x: x[Phase.BEFORE], axis=1, result_type='expand')
    a = results.apply(lambda x: x[Phase.AFTER], axis=1, result_type='expand')
    d = a.sub(b)
    g = d.apply(lambda x: x.name.gcost * x, axis=1)
    r = d.apply(lambda x: x.name.rcost * x, axis=1)
    keys = ['before', 'after', 'deaths', 'gold', 'resources']

    return pd.concat([b, a, d, g, r], keys=keys)


def unit_losses(logs: ParsedLogs) -> pd.DataFrame:
    """
    Calculates Unit losses by army.
    :param df: Battle Log DataFrame
    :param army: One of the Nations participating in the battle
    :return: DataFrame with calculated unit losses
    """

    attacker_units = unit_results(logs, logs.attacker)
    attacker = unit_dataframe(attacker_units)

    defender_units = unit_results(logs, logs.defender)
    defender = unit_dataframe(defender_units)

    keys = [logs.attacker.name, logs.defender.name]
    return pd.concat([attacker, defender], keys=keys)


def results(results: ParsedLogs) -> Results:

    win_score = wins(results)
    units_df = unit_losses(results)

    return Results(attacker=results.attacker,
                   defender=results.defender,
                   win_score=win_score,
                   unit_losses=units_df)
