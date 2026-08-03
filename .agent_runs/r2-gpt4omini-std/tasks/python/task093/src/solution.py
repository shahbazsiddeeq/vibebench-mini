# src/solution.py

class EventBus:
    def __init__(self):
        self._handlers = {}

    def subscribe(self, event, handler):
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def unsubscribe(self, event, handler):
        if event in self._handlers:
            self._handlers[event].remove(handler)
            if not self._handlers[event]:
                del self._handlers[event]

    def publish(self, event, data=None):
        if event in self._handlers:
            for handler in self._handlers[event]:
                handler(data)
