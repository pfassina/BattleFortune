from dataclasses import dataclass

import pandas as pd
from pandas.compat import os

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


@dataclass
class Calculator:
    parsed_logs: ParsedLogs

    @property
    def simulations(self) -> int:
        return self.parsed_logs.simulations

    @property
    def winners(self) -> dict[Nation, list[bool]]:
        return self.parsed_logs.winners

    @property
    def attacker(self) -> Nation:
        return self.parsed_logs.attacker

    @property
    def defender(self) -> Nation:
        return self.parsed_logs.defender

    @property
    def win_count(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.winners, orient="index")
        df_csv = df.reset_index()
        df_csv.columns = ["nation"] + [f"sim_{s + 1}" for s in range(self.simulations)]

        file_path = os.path.join("csv", "win_score.csv")
        df_csv.to_csv(file_path)
        return df.sum(axis=1)

    @property
    def unit_losses(self) -> pd.DataFrame:
        attacker_units = self.unit_results(self.attacker)
        attacker = self.unit_dataframe(attacker_units)

        defender_units = self.unit_results(self.defender)
        defender = self.unit_dataframe(defender_units)

        keys = [self.attacker.name, self.defender.name]
        df = pd.concat([attacker, defender], keys=keys)
        df_csv = df.reset_index()
        df_csv.columns = ["nation", "dimension", "unit"] + [
            f"sim_{s + 1}" for s in range(self.simulations)
        ]

        file_path = os.path.join("csv", "unit_losses.csv")
        df_csv.to_csv(file_path)
        return df

    def unit_results(self, nation: Nation) -> pd.DataFrame:
        battles = self.parsed_logs.battles[nation]
        results = {unit: battles[unit] for unit in self.parsed_logs.units(nation)}
        return pd.DataFrame.from_dict(results, orient="index")

    def unit_dataframe(self, results: pd.DataFrame) -> pd.DataFrame:
        before = results.apply(lambda x: x[Phase.BEFORE], axis=1, result_type="expand")
        after = results.apply(lambda x: x[Phase.AFTER], axis=1, result_type="expand")
        deaths = after.sub(before)
        gold = deaths.apply(lambda x: x.name.gcost * x, axis=1)
        resources = deaths.apply(lambda x: x.name.rcost * x, axis=1)
        keys = ["before", "after", "deaths", "gold", "resources"]
        df = pd.DataFrame(
            pd.concat([before, after, deaths, gold, resources], keys=keys)
        )
        return df

    @property
    def results(self) -> Results:
        return Results(self.attacker, self.defender, self.win_count, self.unit_losses)


def results(parsed_logs: ParsedLogs) -> Results:
    calculator = Calculator(parsed_logs)
    return calculator.results
