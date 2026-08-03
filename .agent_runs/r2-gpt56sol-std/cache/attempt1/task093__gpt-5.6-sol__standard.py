"""A simple synchronous event bus."""

from collections.abc import Callable, Hashable
from typing import Any


class EventBus:
    """Publish events to handlers in subscription order."""

    def __init__(self) -> None:
        self._handlers: dict[Hashable, list[Callable[[Any], Any]]] = {}

    def subscribe(self, event: Hashable, handler: Callable[[Any], Any]) -> None:
        """Subscribe a handler to an event."""
        self._handlers.setdefault(event, []).append(handler)

    def unsubscribe(self, event: Hashable, handler: Callable[[Any], Any]) -> None:
        """Remove one matching handler subscription, if present."""
        handlers = self._handlers.get(event)
        if not handlers:
            return

        try:
            handlers.remove(handler)
        except ValueError:
            return

        if not handlers:
            del self._handlers[event]

    def publish(self, event: Hashable, data: Any = None) -> None:
        """Synchronously call subscribed handlers in subscription order."""
        for handler in tuple(self._handlers.get(event, ())):
            handler(data)
