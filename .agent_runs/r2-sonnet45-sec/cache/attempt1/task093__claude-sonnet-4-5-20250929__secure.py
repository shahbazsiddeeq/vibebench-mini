class EventBus:
    """
    A simple event bus implementation that allows subscribing to events,
    unsubscribing from events, and publishing events to all subscribers.
    """
    
    def __init__(self):
        """Initialize the event bus with an empty handlers dictionary."""
        self._handlers = {}
    
    def subscribe(self, event, handler):
        """
        Subscribe a handler to an event.
        
        Args:
            event: The event name (string)
            handler: A callable that will be invoked when the event is published
        
        Raises:
            TypeError: If event is not a string or handler is not callable
        """
        if not isinstance(event, str):
            raise TypeError("Event must be a string")
        if not callable(handler):
            raise TypeError("Handler must be callable")
        
        if event not in self._handlers:
            self._handlers[event] = []
        
        self._handlers[event].append(handler)
    
    def unsubscribe(self, event, handler):
        """
        Unsubscribe a handler from an event.
        
        Args:
            event: The event name (string)
            handler: The callable to remove from the event's handlers
        
        Raises:
            TypeError: If event is not a string
        """
        if not isinstance(event, str):
            raise TypeError("Event must be a string")
        
        if event in self._handlers:
            try:
                self._handlers[event].remove(handler)
            except ValueError:
                # Handler not in list, silently ignore
                pass
            
            # Clean up empty handler lists
            if not self._handlers[event]:
                del self._handlers[event]
    
    def publish(self, event, data=None):
        """
        Publish an event, calling all subscribed handlers synchronously.
        
        Args:
            event: The event name (string)
            data: Optional data to pass to handlers (default: None)
        
        Raises:
            TypeError: If event is not a string
        """
        if not isinstance(event, str):
            raise TypeError("Event must be a string")
        
        if event not in self._handlers:
            return
        
        # Create a copy of the handlers list to avoid issues if handlers
        # modify the subscription list during iteration
        handlers = self._handlers[event][:]
        
        for handler in handlers:
            try:
                handler(data)
            except Exception:
                # Silently catch exceptions in handlers to prevent one
                # handler from breaking others. In production, you might
                # want to log these errors.
                pass
