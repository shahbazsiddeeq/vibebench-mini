class EventBus:
    def __init__(self):
        self.handlers = {}
    
    def subscribe(self, event, handler):
        if event not in self.handlers:
            self.handlers[event] = []
        self.handlers[event].append(handler)
    
    def unsubscribe(self, event, handler):
        if event in self.handlers:
            if handler in self.handlers[event]:
                self.handlers[event].remove(handler)
    
    def publish(self, event, data=None):
        if event in self.handlers:
            # Create a copy of the handlers list to avoid issues if handlers
            # modify the list during iteration (e.g., unsubscribing themselves)
            handlers_copy = self.handlers[event][:]
            for handler in handlers_copy:
                # Check if handler is still subscribed (in case it was removed)
                if handler in self.handlers.get(event, []):
                    handler(data)
