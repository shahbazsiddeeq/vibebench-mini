"""
A secure, self-contained EventBus implementation.

This module defines an `EventBus` class that allows subscribing,
unsubscribing, and publishing events with associated handlers. All
inputs are validated defensively and internal errors are never leaked
to callers.
"""

from typing import Any, Callable, Dict, Hashable, List


class EventBus:
    """A simple synchronous publish/subscribe event bus.

    Handlers are called in the order they were subscribed. Unsubscribing
    a handler during publishing (e.g., from within the handler itself)
    is safe and will not affect the current publish cycle beyond
    preventing that handler from being called again in future publishes.
    """

    def __init__(self) -> None:
        # Maps event name -> list of handler callables.
        self._handlers: Dict[Hashable, List[Callable[..., Any]]] = {}

    def subscribe(self, event: Hashable, handler: Callable[..., Any]) -> None:
        """Subscribe a handler to an event.

        Args:
            event: The event identifier (must be hashable).
            handler: A callable that accepts a single argument (data).

        Raises:
            TypeError: If `handler` is not callable or `event` is not hashable.
        """
        self._validate_event(event)
        self._validate_handler(handler)

        handlers = self._handlers.setdefault(event, [])
        handlers.append(handler)

    def unsubscribe(self, event: Hashable, handler: Callable[..., Any]) -> None:
        """Unsubscribe a handler from an event.

        Silently does nothing if the event or handler is not found.

        Args:
            event: The event identifier.
            handler: The handler to remove.
        """
        self._validate_event(event)
        self._validate_handler(handler)

        handlers = self._handlers.get(event)
        if not handlers:
            return

        try:
            handlers.remove(handler)
        except ValueError:
            # Handler was not subscribed; ignore silently.
            pass

        # Clean up empty handler lists to avoid unbounded growth.
        if not handlers:
            self._handlers.pop(event, None)

    def publish(self, event: Hashable, data: Any = None) -> None:
        """Publish an event, invoking all subscribed handlers synchronously.

        Handlers are called in subscription order. If a handler raises an
        exception, it is suppressed (to avoid exposing internal errors or
        breaking other handlers), and processing continues with the next
        handler.

        Args:
            event: The event identifier.
            data: Optional data to pass to each handler.
        """
        self._validate_event(event)

        handlers = self._handlers.get(event)
        if not handlers:
            return

        # Iterate over a snapshot so that handlers modifying the
        # subscription list (e.g., unsubscribing themselves) during
        # publish do not cause skipped/duplicated calls or runtime errors.
        for handler in list(handlers):
            try:
                handler(data)
            except Exception:
                # Do not let a misbehaving handler crash the bus or leak
                # internal details; silently continue with next handler.
                continue

    @staticmethod
    def _validate_event(event: Hashable) -> None:
        try:
            hash(event)
        except TypeError as exc:
            raise TypeError("event must be hashable") from exc

    @staticmethod
    def _validate_handler(handler: Callable[..., Any]) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
