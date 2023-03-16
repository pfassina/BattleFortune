import sys
from enum import StrEnum, auto
from typing import Protocol


class OS(StrEnum):
    WIN32 = auto()
    DARWIN = auto()


class PlatformProtocol(Protocol):
    def run_command(self, sim_name: str, host_game: bool) -> list[str]:
        ...

    def get_app_window(self) -> tuple[int, int]:
        ...

    def kill_process(self, pid: int) -> None:
        ...

def get_platform() -> PlatformProtocol:
    if sys.platform == OS.DARWIN:
        from src.platforms.darwin import Darwin

        return Darwin()

    if sys.platform == OS.WIN32:
        from src.platforms.windows import Windows

        return Windows()

    raise NotImplemented
