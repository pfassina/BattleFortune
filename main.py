import os

import psutil

from src import gui


def has_instance() -> bool:
    return "BattleFortune" in [p.info["name"] for p in psutil.process_iter(["name"])]  # type: ignore


def main() -> None:
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if has_instance():
        return

    gui.start()


if __name__ == "__main__":
    main()
