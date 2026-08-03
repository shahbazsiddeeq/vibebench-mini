"""
Observer Pattern implementation.

This module provides a Subject class that manages observers and notifies them
of events, along with an Observer base class that observers should inherit from.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class Observer(ABC):
    """
    Abstract base class for observers in the Observer pattern.
    
    Observers should inherit from this class and implement the update method
    to handle notifications from subjects.
    """
    
    @abstractmethod
    def update(self, event: str, data: Any = None) -> None:
        """
        Called when the subject notifies observers of an event.
        
        Args:
            event: A string identifier for the event type.
            data: Optional data associated with the event.
        """
        pass


class Subject:
    """
    Subject class that manages observers and notifies them of events.
    
    The Subject maintains a list of attached observers and can notify them
    all when an event occurs.
    """
    
    def __init__(self) -> None:
        """Initialize the Subject with an empty list of observers."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to this subject.
        
        Args:
            observer: An Observer instance to attach.
            
        Raises:
            TypeError: If observer is not an instance of Observer.
            ValueError: If observer is None.
        """
        if observer is None:
            raise ValueError("Observer cannot be None")
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an instance of Observer")
        
        # Avoid duplicate attachments
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from this subject.
        
        Args:
            observer: An Observer instance to detach.
            
        Raises:
            TypeError: If observer is not an instance of Observer.
        """
        if observer is None:
            return
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an instance of Observer")
        
        # Remove observer if it exists in the list
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: str, data: Any = None) -> None:
        """
        Notify all attached observers of an event.
        
        Args:
            event: A string identifier for the event type.
            data: Optional data to pass to observers.
            
        Raises:
            TypeError: If event is not a string.
        """
        if not isinstance(event, str):
            raise TypeError("event must be a string")
        
        # Notify all observers
        for observer in self._observers:
            observer.update(event, data)
