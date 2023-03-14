from dataclasses import dataclass, field
import json
import os


@dataclass
class Nation:
    nation_id: int
    name: str = field(init=False)
    era: int = field(init=False)

    def __post_init__(self):

        nations_path = os.path.join('data', 'nations.json')
        with open(nations_path, 'r') as file:
            nation_stats = json.load(file)[str(self.nation_id)]

        self.name: str = nation_stats['name']
        self.era: int = int(nation_stats['era'])

    def __eq__(self, other) -> bool:
        return self.nation_id == other.nation_id

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.nation_id)


@dataclass
class Unit:
    name: str
    unit_id: int = field(init=False)
    gcost: int = field(init=False)
    rcost: int = field(init=False)

    def __post_init__(self) -> None:
        units_path = os.path.join('data', 'units.json')
        with open(units_path, 'r') as file:
            unit_stats = json.load(file)[self.name]

        self.unit_id: int = int(unit_stats['id'])
        gcost = unit_stats['gcost']
        rcost = unit_stats['rcost']

        self.gcost: int = int(gcost) if gcost != 'undefined' else 0
        self.rcost: int = int(rcost) if rcost != 'undefined' else 0

    def __eq__(self, other) -> bool:
        return self.unit_id == other.unit_id

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.unit_id)
