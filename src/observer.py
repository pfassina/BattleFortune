from typing import Callable, Optional


class Subject:
    def __init__(self) -> None:
        self._observers: list[Callable] = []

    def attach(self, observer: Callable):
        self._observers.append(observer)

    def detach(self, observer: Callable):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer(message)


SUBJECT: Optional[Subject]


def init() -> None:
    global SUBJECT

    SUBJECT = None
