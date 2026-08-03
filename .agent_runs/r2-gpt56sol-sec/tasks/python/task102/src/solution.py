from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    @abstractmethod
    def update(self, event: Any, data: Any) -> None:
        """Receive a notification from a subject."""
        raise NotImplementedError


class Subject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an Observer instance")
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an Observer instance")
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event: Any, data: Any = None) -> None:
        for observer in tuple(self._observers):
            observer.update(event, data)
