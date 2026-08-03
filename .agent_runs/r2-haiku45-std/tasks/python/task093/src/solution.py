from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)
    
    def subscribe(self, event, handler):
        """Subscribe a handler to an event."""
        self._handlers[event].append(handler)
    
    def unsubscribe(self, event, handler):
        """Unsubscribe a handler from an event."""
        if event in self._handlers:
            try:
                self._handlers[event].remove(handler)
            except ValueError:
                pass
    
    def publish(self, event, data=None):
        """Publish an event, calling all subscribed handlers synchronously."""
        if event in self._handlers:
            # Create a copy of the handlers list to avoid issues if handlers
            # unsubscribe themselves during iteration
            handlers_copy = self._handlers[event][:]
            for handler in handlers_copy:
                handler(data)
