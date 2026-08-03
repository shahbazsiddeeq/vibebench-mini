"""Synchronous event bus implementation."""

from __future__ import annotations

from collections.abc import Callable, Hashable
from threading import RLock
from typing import Any


class EventBus:
    """A synchronous, subscription-ordered event bus."""

    def __init__(self) -> None:
        self._handlers: dict[Hashable, list[Callable[[Any], Any]]] = {}
        self._lock = RLock()

    @staticmethod
    def _validate_event(event: object) -> None:
        try:
            hash(event)
        except (TypeError, ValueError):
            raise TypeError("event must be hashable") from None

    def subscribe(
        self, event: Hashable, handler: Callable[[Any], Any]
    ) -> None:
        """Subscribe a callable handler to an event."""
        self._validate_event(event)
        if not callable(handler):
            raise TypeError("handler must be callable")

        with self._lock:
            self._handlers.setdefault(event, []).append(handler)

    def unsubscribe(
        self, event: Hashable, handler: Callable[[Any], Any]
    ) -> None:
        """Remove one matching handler subscription, if present."""
        self._validate_event(event)
        if not callable(handler):
            raise TypeError("handler must be callable")

        with self._lock:
            handlers = self._handlers.get(event)
            if not handlers:
                return

            for index, subscribed_handler in enumerate(handlers):
                if subscribed_handler is handler or subscribed_handler == handler:
                    del handlers[index]
                    if not handlers:
                        del self._handlers[event]
                    return

    def publish(self, event: Hashable, data: Any = None) -> None:
        """Synchronously call handlers in their subscription order."""
        self._validate_event(event)

        with self._lock:
            handlers = tuple(self._handlers.get(event, ()))

        for handler in handlers:
            handler(data)
