import logging
import os

from src import gui, observer


def set_cwd() -> None:
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def set_logging() -> None:
    logging.basicConfig(
        filename="battlefortune.log",
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def set_dir_structure() -> None:
    directories = ["data", "logs", "img", "csv"]
    for dir in directories:
        if os.path.exists(dir):
            continue
        os.mkdir(dir)


def set_observer() -> None:
    observer.init()
    observer.SUBJECT = observer.Subject()


def main() -> None:
    # initial project structure
    set_cwd()
    set_logging()
    set_dir_structure()
    # set_observer()

    logging.info("starting gui application")
    gui.start()


if __name__ == "__main__":
    main()
