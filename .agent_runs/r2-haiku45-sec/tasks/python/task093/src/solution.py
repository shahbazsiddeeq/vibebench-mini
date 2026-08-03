"""
EventBus module for managing event subscriptions and publishing.
"""

from collections import defaultdict
from typing import Callable, Any, Optional


class EventBus:
    """
    A simple event bus for subscribing to events and publishing data to handlers.
    
    Handlers are called synchronously in the order they were subscribed.
    """
    
    def __init__(self) -> None:
        """Initialize the EventBus with an empty handler registry."""
        self._handlers: dict[str, list[Callable[[Any], None]]] = defaultdict(list)
    
    def subscribe(self, event: str, handler: Callable[[Any], None]) -> None:
        """
        Subscribe a handler to an event.
        
        Args:
            event: The event name to subscribe to.
            handler: A callable that will be invoked when the event is published.
        
        Raises:
            TypeError: If event is not a string or handler is not callable.
        """
        if not isinstance(event, str):
            raise TypeError("Event name must be a string")
        if not callable(handler):
            raise TypeError("Handler must be callable")
        
        self._handlers[event].append(handler)
    
    def unsubscribe(self, event: str, handler: Callable[[Any], None]) -> None:
        """
        Unsubscribe a handler from an event.
        
        Args:
            event: The event name to unsubscribe from.
            handler: The handler to remove.
        
        Raises:
            TypeError: If event is not a string.
        """
        if not isinstance(event, str):
            raise TypeError("Event name must be a string")
        
        if event in self._handlers:
            try:
                self._handlers[event].remove(handler)
            except ValueError:
                # Handler not found, silently ignore
                pass
    
    def publish(self, event: str, data: Any = None) -> None:
        """
        Publish an event, calling all subscribed handlers synchronously.
        
        Args:
            event: The event name to publish.
            data: Optional data to pass to the handlers.
        
        Raises:
            TypeError: If event is not a string.
        """
        if not isinstance(event, str):
            raise TypeError("Event name must be a string")
        
        if event in self._handlers:
            # Create a copy of the handlers list to allow handlers to unsubscribe
            # themselves during iteration
            handlers_copy = self._handlers[event].copy()
            for handler in handlers_copy:
                # Only call if handler is still in the list (in case it unsubscribed itself)
                if handler in self._handlers[event]:
                    handler(data)
