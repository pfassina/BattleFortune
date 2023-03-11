from dataclasses import dataclass

import pandas as pd

from src.decode import Nation
from src.read import ParsedLogs, Phase


@dataclass
class Results:
    attacker: Nation
    defender: Nation
    win_score: pd.DataFrame
    unit_losses: pd.DataFrame

    @property
    def army_cost(self) -> pd.DataFrame:
        return self.unit_losses.groupby(level=[0, 1]).sum()  # type: ignore


def wins(logs: ParsedLogs) -> pd.DataFrame:
    """
    Parses a list of WinLogs and calculates the ratio of winnings per Nation.
    :return: DataFrame with Win Counts per Nation.
    """

    df = pd.DataFrame.from_dict(logs.winners, orient="index")
    df_csv = df.reset_index()
    df_csv.columns = ["nation"] + [f"sim_{s + 1}" for s in range(logs.simulations)]
    df_csv.to_csv("./csv/win_score.csv")
    return df.sum(axis=1)


def unit_results(logs: ParsedLogs, nation: Nation) -> pd.DataFrame:
    battles = logs.battles[nation]
    results = {unit: battles[unit] for unit in logs.units(nation)}
    return pd.DataFrame.from_dict(results, orient="index")


def unit_dataframe(results: pd.DataFrame) -> pd.DataFrame:
    before = results.apply(lambda x: x[Phase.BEFORE], axis=1, result_type="expand")
    after = results.apply(lambda x: x[Phase.AFTER], axis=1, result_type="expand")
    deaths = after.sub(before)
    gold = deaths.apply(lambda x: x.name.gcost * x, axis=1)
    resources = deaths.apply(lambda x: x.name.rcost * x, axis=1)
    keys = ["before", "after", "deaths", "gold", "resources"]
    df = pd.DataFrame(pd.concat([before, after, deaths, gold, resources], keys=keys))

    return df


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
    df = pd.concat([attacker, defender], keys=keys)
    df_csv = df.reset_index()
    df_csv.columns = ["nation", "dimension", "unit"] + [
        f"sim_{s + 1}" for s in range(logs.simulations)
    ]
    df_csv.to_csv("./csv/unit_losses.csv")
    return df


def results(results: ParsedLogs) -> Results:
    win_score = wins(results)
    units_df = unit_losses(results)

    return Results(
        attacker=results.attacker,
        defender=results.defender,
        win_score=win_score,
        unit_losses=units_df,
    )
