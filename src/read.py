import os
from dataclasses import dataclass
from enum import Enum

import yaml

from src.config import CONFIG
from src.decode import Nation, Unit


class Phase(Enum):
    BEFORE = "before"
    AFTER = "after"

    def __str__(self) -> str:
        return self.value


class Role(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"

    def __str__(self) -> str:
        return self.value


@dataclass
class BattleEntry:
    nation: Nation
    unit: Unit
    phase: Phase
    count: int


@dataclass
class BattleLog:
    entries: list[BattleEntry]

    @property
    def nations(self) -> set[Nation]:
        return set([e.nation for e in self.entries])

    def units(self, nation: Nation) -> set[Unit]:
        return set(e.unit for e in self.entries if e.nation == nation)

    def find_entry(self, nation: Nation, unit: Unit, phase: Phase) -> int:
        return next(
            (
                e.count
                for e in self.entries
                if e.nation == nation and e.unit == unit and e.phase == phase
            ),
            0,
        )

    @property
    def results(self) -> dict[Nation, dict[Unit, dict[Phase, int]]]:
        return {
            nation: {
                unit: {
                    Phase.BEFORE: self.find_entry(nation, unit, Phase.BEFORE),
                    Phase.AFTER: self.find_entry(nation, unit, Phase.AFTER),
                }
                for unit in self.units(nation)
            }
            for nation in self.nations
        }


@dataclass
class Log:
    attacker_id: int
    defender_id: int
    turn: int
    winner_id: int
    battle_log: BattleLog

    @property
    def nations(self) -> dict[Role, Nation]:
        return {
            Role.ATTACKER: Nation(self.attacker_id),
            Role.DEFENDER: Nation(self.defender_id),
        }


@dataclass
class ParsedLogs:
    logs: list[Log]

    @property
    def simulations(self) -> int:
        return len(self.battle_logs)

    @property
    def battle_logs(self) -> list[BattleLog]:
        return [log.battle_log for log in self.logs]

    @property
    def nations(self) -> dict[Role, Nation]:
        return self.logs[0].nations

    @property
    def attacker(self) -> Nation:
        return self.nations[Role.ATTACKER]

    @property
    def defender(self) -> Nation:
        return self.nations[Role.DEFENDER]

    @property
    def winners(self) -> dict[Nation, list[bool]]:
        attacker = self.nations[Role.ATTACKER]
        defender = self.nations[Role.DEFENDER]

        attacker_wins = [
            True if log.winner_id == attacker.nation_id else False for log in self.logs
        ]
        defender_wins = [
            True if log.winner_id == defender.nation_id else False for log in self.logs
        ]

        return {attacker: attacker_wins, defender: defender_wins}

    def units(self, nation: Nation) -> set[Unit]:
        return set.union(*[log.battle_log.units(nation) for log in self.logs])

    @staticmethod
    def find_entry(entry: BattleLog, nation: Nation, unit: Unit, phase: Phase):
        return entry.results.get(nation, {}).get(unit, {}).get(phase, 0)

    @property
    def battles(self) -> dict[Nation, dict[Unit, dict[Phase, list[int]]]]:
        return {
            nation: {
                unit: {
                    Phase.BEFORE: [
                        self.find_entry(bl, nation, unit, Phase.BEFORE)
                        for bl in self.battle_logs
                    ],
                    Phase.AFTER: [
                        self.find_entry(bl, nation, unit, Phase.AFTER)
                        for bl in self.battle_logs
                    ],
                }
                for unit in self.units(nation)
            }
            for nation in self.nations.values()
        }

    def dump_to_yaml(self) -> None:
        log_path = os.path.join("logs", CONFIG.data.game_name)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        with open(os.path.join(log_path, "nations.yaml"), "w") as file:
            nation_roles = {
                Role.ATTACKER.value: self.nations[Role.ATTACKER].name,
                Role.DEFENDER.value: self.nations[Role.DEFENDER].name,
            }

            yaml.dump(data=nation_roles, stream=file)

        with open(os.path.join(log_path, "winners.yaml"), "w") as file:
            winners_yaml = {
                nation.name: [score for score in self.winners[nation]]
                for nation in self.winners
            }
            yaml.dump(data=winners_yaml, stream=file)

        with open(os.path.join(log_path, "battles.yaml"), "w") as file:
            battle_yaml = {
                nation.name: {
                    unit.name: {
                        phase.value: results for phase, results in phases.items()
                    }
                    for unit, phases in units.items()
                }
                for nation, units in self.battles.items()
            }

            yaml.dump(data=battle_yaml, stream=file)


@dataclass
class Parser:
    turns: list[int]

    def parse_log(self, turn: int) -> Log:
        # get battle log
        log_path = os.path.join(CONFIG.data.simulation_path(turn), "log.txt")
        with open(log_path, mode="r") as file:
            log = file.read()

        # identify armies
        attacker, defender = self.parse_nations(log)

        return Log(
            attacker_id=attacker,
            defender_id=defender,
            turn=turn,
            winner_id=self.parse_winner(log, attacker, defender),
            battle_log=self.parse_battle(log, attacker, defender),
        )

    @property
    def parsed_logs(self) -> ParsedLogs:
        return ParsedLogs([self.parse_log(t) for t in self.turns])

    def parse_nations(self, log: str) -> tuple[int, int]:
        armies = log[log.find("getbattlecount:") + 15 :].split(",", 3)[1:3]
        defender = False if armies[0].find("def") == -1 else True

        try:
            a, b = [int(a.strip().split(" ")[1]) for a in armies]

        except:
            print(log)
            raise ValueError

        return (b, a) if defender else (a, b)

    def parse_winner(self, log, attacker_id: int, defender_id: int) -> int:
        # parse log to find player nation
        player_blurb = log.find("got turn info for player")
        player = int(log[player_blurb + 25 :].split("\n")[0])

        # Define Winner based on Province Defense at Battle Province
        if log.find("whatPD") > 0:  # Player can add PD
            return attacker_id if player == attacker_id else defender_id

        return defender_id if player == attacker_id else defender_id

    def parse_battle(self, log, attacker_id: int, defender_id: int) -> BattleLog:
        entries = [
            self.parse_battle_entry(attacker_id, defender_id, i)
            for i in self.find_battle(log)
        ]

        return BattleLog(entries)

    def parse_battle_entry(
        self, attacker_id: int, defender_id: int, blurb: str
    ) -> BattleEntry:
        cleaned_blurb = blurb.split("(")[0].strip()
        nation_blurb, unit_blurb = [i.strip() for i in cleaned_blurb.split(":")]

        nation = attacker_id if nation_blurb in ["0", "1"] else defender_id
        unit = Unit(unit_blurb.split(" ", 2)[2])
        phase = Phase.BEFORE if nation_blurb in ["0", "2"] else Phase.AFTER
        count = sum([int(i) for i in unit_blurb.split(" ", 2)[:2]])

        return BattleEntry(Nation(nation), unit, phase, count)

    def find_battle(self, log) -> list[str]:
        start = log.find("getbattlecountfromvcr") + 21
        end = log.rfind("restoremonarrays")

        return log[start : end - 1].split("\n")[1:]


def combine_logs(turns: list[int]) -> ParsedLogs:
    parser = Parser(turns)
    parsed_logs = parser.parsed_logs
    parsed_logs.dump_to_yaml()

    return parsed_logs
