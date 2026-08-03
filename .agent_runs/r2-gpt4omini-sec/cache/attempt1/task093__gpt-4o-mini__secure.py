# src/solution.py

class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event: str, handler: callable) -> None:
        if not isinstance(event, str) or not callable(handler):
            raise ValueError("Invalid event or handler")
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(handler)

    def unsubscribe(self, event: str, handler: callable) -> None:
        if not isinstance(event, str) or not callable(handler):
            raise ValueError("Invalid event or handler")
        if event in self._subscribers:
            self._subscribers[event] = [
                h for h in self._subscribers[event] if h is not handler
            ]

    def publish(self, event: str, data=None) -> None:
        if not isinstance(event, str):
            raise ValueError("Invalid event")
        if event in self._subscribers:
            for handler in self._subscribers[event]:
                handler(data)
