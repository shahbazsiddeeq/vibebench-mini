class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event, handler):
        if event not in self._subscribers:
            self._subscribers[event] = []
        if handler not in self._subscribers[event]:
            self._subscribers[event].append(handler)

    def unsubscribe(self, event, handler):
        if event in self._subscribers:
            # Create a new list without the handler to avoid issues during iteration
            # if unsubscribe is called from within a handler during publish.
            self._subscribers[event] = [h for h in self._subscribers[event] if h != handler]
            if not self._subscribers[event]:
                del self._subscribers[event]

    def publish(self, event, data=None):
        if event in self._subscribers:
            # Iterate over a copy of the list of handlers to prevent issues
            # if handlers unsubscribe themselves during the publish cycle.
            handlers_to_call = list(self._subscribers[event])
            for handler in handlers_to_call:
                # Check if the handler is still subscribed before calling it.
                # This handles cases where a handler unsubscribes itself or another handler
                # that was further down in the original list.
                if event in self._subscribers and handler in self._subscribers[event]:
                    handler(data)
