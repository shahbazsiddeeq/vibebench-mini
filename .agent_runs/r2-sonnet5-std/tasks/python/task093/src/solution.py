"""Event Bus implementation."""

from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event, handler):
        self._handlers[event].append(handler)

    def unsubscribe(self, event, handler):
        if event in self._handlers and handler in self._handlers[event]:
            self._handlers[event].remove(handler)

    def publish(self, event, data=None):
        handlers = list(self._handlers.get(event, []))
        for handler in handlers:
            handler(data)
