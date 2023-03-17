import asyncio
import logging
import os
import subprocess
from dataclasses import dataclass, field

from tqdm import tqdm

from src.config import CONFIG
from src.platform import PlatformProtocol, get_platform
from src.process import TurnRobot


@dataclass
class SimulationRunner:
    platform: PlatformProtocol
    valid_rounds: list[int] = field(default_factory=list)

    async def host_simulation(self, simulation: int) -> int:
        game_name = f"{CONFIG.data.game_name}_{simulation}"
        game_path = f"{CONFIG.data.game_path}_{simulation}"

        ftherland_path = os.path.join(game_path, "ftherlnd")
        start_time = os.path.getmtime(ftherland_path)

        self.run_dominions(game_name, host_game=True)

        while os.path.getmtime(ftherland_path) == start_time:
            continue

        await asyncio.sleep(0.1)

        return simulation

    async def host_simulations(self) -> None:
        tasks = []
        for i in range(CONFIG.data.simulations):
            logging.info(f"simulation {i} created")
            task = asyncio.create_task(self.host_simulation(i + 1))
            tasks.append(task)

        for task in asyncio.as_completed(tasks):
            simulation = await task
            if simulation is not None:
                logging.info(f"hosting simulation {simulation} completed")
                self.valid_rounds.append(simulation)

    def batch_process(self) -> None:
        logging.info("simulation processing")
        for r in tqdm(self.valid_rounds):
            sim_name = f"{CONFIG.data.game_name}_{r}"
            pid = self.run_dominions(sim_name, False)
            robot = TurnRobot(self.platform, r, pid)
            robot.process_turn()
            logging.info(f"processing of simulation {sim_name} completed")

    def run_dominions(self, sim_name: str, host_game: bool) -> int:
        cmd = self.platform.run_command(sim_name, host_game)
        if host_game:
            logging.info(f"hosting simulation {sim_name}")
            return subprocess.Popen(cmd, cwd=CONFIG.data.dominions_path).pid

        logging.info(f"processing simulaton {sim_name}")
        log_path = os.path.join(CONFIG.data.dominions_path, "log.txt")
        with open(log_path, "w") as log:
            return subprocess.Popen(cmd, cwd=CONFIG.data.dominions_path, stdout=log).pid


def simulation() -> list[int]:
    logging.info("starting simulations")
    platform = get_platform()
    logging.info(f"platform detected: {platform}")
    sim_runner = SimulationRunner(platform)
    logging.info(f"starting simulations")
    asyncio.run(sim_runner.host_simulations())
    sim_runner.batch_process()

    return sim_runner.valid_rounds
