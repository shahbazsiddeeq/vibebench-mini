from __future__ import annotations

from collections import defaultdict
from typing import Callable


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable) -> None:
        self._handlers[event].append(handler)

    def unsubscribe(self, event: str, handler: Callable) -> None:
        if handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    def publish(self, event: str, data=None) -> None:
        for handler in list(self._handlers[event]):
            handler(data)
