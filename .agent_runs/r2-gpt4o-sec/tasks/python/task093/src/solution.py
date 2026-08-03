# src/solution.py

class EventBus:
    def __init__(self):
        self._handlers = {}

    def subscribe(self, event, handler):
        if not callable(handler):
            raise ValueError("Handler must be callable")
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append(handler)

    def unsubscribe(self, event, handler):
        if event in self._handlers:
            try:
                self._handlers[event].remove(handler)
                if not self._handlers[event]:
                    del self._handlers[event]
            except ValueError:
                pass  # Handler not found, do nothing

    def publish(self, event, data=None):
        if event in self._handlers:
            # Create a copy of the list to prevent modification during iteration
            handlers = list(self._handlers[event])
            for handler in handlers:
                try:
                    handler(data)
                except Exception:
                    pass  # Silently ignore exceptions in handlers
