import os
import time
from dataclasses import dataclass
from enum import Enum

import yaml

from src.config import SimConfig
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
        """
        returns dict containing a unit count for each nation, unit, and phase.
        """
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

    def dump_to_yaml(self, game_name: str) -> None:
        log_path = os.path.join("logs", game_name)
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


def validate_log(dominions_path: str) -> bool:
    """
    Checks if Log finished loading.
    :return: True if log is valid
    """

    start_time = time.time()
    while time.time() - start_time <= 10:  # max wait time is 10 seconds
        with open(f"{dominions_path}/log.txt", "r") as file:
            log = file.read()

        start = log.rfind("getbattlecountfromvcr")
        if start == -1:
            continue

        if log[start:].rfind("whatPD") != -1:  # Player Won
            return True

        if log[start:].rfind("[eof]") != -1:  # Player Lost
            return True

    return False


def parse_nations(log: str) -> tuple[int, int]:
    """
    Parses Nations from Log.
    :param log: log file
    :return: Dictionary with Nations Ids
    """

    armies = log[log.find("getbattlecount:") + 15 :].split(",", 3)[1:3]
    defender = False if armies[0].find("def") == -1 else True

    try:
        a, b = [int(a.strip().split(" ")[1]) for a in armies]

    except:
        print(log)
        raise ValueError

    return (b, a) if defender else (a, b)


def find_battle(log) -> list[str]:
    """
    Find Battle log blurb
    :param log: log file
    :return: battle log blurb
    """

    start = log.find("getbattlecountfromvcr") + 21
    end = log.rfind("restoremonarrays")

    return log[start : end - 1].split("\n")[1:]


def parse_battle_entry(attacker_id: int, defender_id: int, blurb: str) -> BattleEntry:
    """
    parse battle entry from battle log
    :param simulation_round:  Simulation Round
    :param attacker: attacker nation id
    :param defender: defender nation id
    :param battle_entry: entry on battle log
    :return: dictionary with battle entry results
    """

    cleaned_blurb = blurb.split("(")[0].strip()
    nation_blurb, unit_blurb = [i.strip() for i in cleaned_blurb.split(":")]

    nation = attacker_id if nation_blurb in ["0", "1"] else defender_id
    unit = Unit(unit_blurb.split(" ", 2)[2])
    phase = Phase.BEFORE if nation_blurb in ["0", "2"] else Phase.AFTER
    count = sum([int(i) for i in unit_blurb.split(" ", 2)[:2]])

    return BattleEntry(Nation(nation), unit, phase, count)


def parse_battle(log, attacker_id: int, defender_id: int) -> BattleLog:
    """
    Parses Battle Blurb
    :param simulation_round: Simulation Round
    :param log: log file
    :param attacker: attacker nation id
    :param defender: defender nation id
    :return: battle log
    """

    entries = [
        parse_battle_entry(attacker_id, defender_id, i) for i in find_battle(log)
    ]

    return BattleLog(entries)


def parse_winner(log, attacker_id: int, defender_id: int) -> int:
    """
    parses round winner from log
    :param simulation_round: simulation round
    :param log: log file
    :param attacker: attacker nation id
    :param defender: defender nation id
    :return: dictionary with the nation that won the turn
    """

    # parse log to find player nation
    player_blurb = log.find("got turn info for player")
    player = int(log[player_blurb + 25 :].split("\n")[0])

    # Define Winner based on Province Defense at Battle Province
    if log.find("whatPD") > 0:  # Player can add PD
        return attacker_id if player == attacker_id else defender_id

    return defender_id if player == attacker_id else defender_id


def parse_log(config: SimConfig, turn: int) -> Log:
    """
    Parses Turn Log and returns turn log dictionary.
    :param simulation_round: Simulation round.
    :return: dictionary with nations, win log and battle log.
    """

    # get battle log
    log_path = os.path.join(config.simulation_path(turn), "log.txt")
    with open(log_path, mode="r") as file:
        log = file.read()

    # identify armies
    attacker, defender = parse_nations(log)

    return Log(
        attacker_id=attacker,
        defender_id=defender,
        turn=turn,
        winner_id=parse_winner(log, attacker, defender),
        battle_log=parse_battle(log, attacker, defender),
    )


def combine_logs(config: SimConfig, turns: list[int]) -> ParsedLogs:
    """
    batch reads logs from all simulations
    :return: log list
    """

    parsed_logs = ParsedLogs([parse_log(config, t) for t in turns])
    parsed_logs.dump_to_yaml(config.game_name)

    return parsed_logs
