import logging
import os

import psutil

from src import gui


def has_instance() -> bool:
    return "BattleFortune" in [p.info["name"] for p in psutil.process_iter(["name"])]  # type: ignore


def main() -> None:
    logging.basicConfig(
        filename="battlefortune.log",
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    logging.info(f"changed path to {dname}")

    logging.info("starting gui application")
    gui.start()


if __name__ == "__main__":
    main()
