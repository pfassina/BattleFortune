import asyncio
import os
import signal
import subprocess
import time
from dataclasses import dataclass, field

from tqdm import tqdm

from src.config import SimConfig
from src.process import TurnRobot


@dataclass
class SimulationRunner:
    config: SimConfig
    valid_rounds: list[int] = field(default_factory=list)

    async def host_simulation(self, simulation: int) -> int:
        game_name = f"{self.config.game_name}_{simulation}"
        game_path = f"{self.config.game_path}_{simulation}"
        ftherland_path = os.path.join(game_path, "ftherlnd")

        start_time = os.path.getmtime(ftherland_path)
        process_id = self.run_dominions(game_name, host_game=True)

        self.wait_for_host(ftherland_path, start_time)

        os.kill(process_id, signal.SIGTERM)
        return simulation

    async def host_simulations(self) -> None:
        tasks = []
        for i in range(self.config.simulations):
            task = asyncio.create_task(self.host_simulation(i + 1))
            tasks.append(task)

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                self.valid_rounds.append(result)

    def wait_for_host(self, path: str, start_time: float) -> bool:
        # Loop until host is finished
        while os.path.getmtime(path) == start_time:
            time.sleep(1)

        return True

    def batch_process(self) -> None:
        for r in tqdm(self.valid_rounds):
            sim_name = f"{self.config.game_name}_{r}"
            pid = self.run_dominions(sim_name, False)
            robot = TurnRobot(self.config, r, pid)
            robot.process_turn()

    def run_dominions(self, sim_name: str, host_game: bool) -> int:
        cmd = self.run_command(sim_name, host_game)
        if host_game:
            return subprocess.Popen(cmd, cwd=self.config.dominions_path).pid

        log_path = os.path.join(self.config.dominions_path, "log.txt")
        with open(log_path, "w") as log:
            return subprocess.Popen(cmd, cwd=self.config.dominions_path, stdout=log).pid

    def run_command(self, sim_name: str, host_game: bool) -> list[str]:
        command = ["./dom5_mac", "--simpgui", "--nosteam"]

        if host_game:
            return command + ["-waxscog", "-T", sim_name]

        return command + ["--res", "960", "720", "-waxscod", sim_name]


def simulation(config: SimConfig) -> list[int]:
    sim_runner = SimulationRunner(config)
    asyncio.run(sim_runner.host_simulations())
    sim_runner.batch_process()

    return sim_runner.valid_rounds
