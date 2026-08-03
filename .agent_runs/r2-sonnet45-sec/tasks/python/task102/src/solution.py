"""
Observer Pattern implementation with Subject and Observer classes.
"""


class Observer:
    """Base class for observers that receive notifications from subjects."""
    
    def update(self, event, data):
        """
        Called when the subject notifies observers of an event.
        
        Args:
            event: The event identifier (typically a string)
            data: Optional data associated with the event
        """
        pass


class Subject:
    """Subject class that maintains a list of observers and notifies them of events."""
    
    def __init__(self):
        """Initialize the subject with an empty list of observers."""
        self._observers = []
    
    def attach(self, observer):
        """
        Attach an observer to this subject.
        
        Args:
            observer: An Observer instance to attach
            
        Raises:
            TypeError: If observer is not an Observer instance
        """
        if not isinstance(observer, Observer):
            raise TypeError("observer must be an instance of Observer")
        
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """
        Detach an observer from this subject.
        
        Args:
            observer: An Observer instance to detach
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event, data=None):
        """
        Notify all attached observers of an event.
        
        Args:
            event: The event identifier to send to observers
            data: Optional data to send with the event (default: None)
        """
        # Create a copy of the observers list to avoid issues if observers
        # modify the list during notification
        observers_copy = self._observers.copy()
        
        for observer in observers_copy:
            try:
                observer.update(event, data)
            except Exception:
                # Silently ignore exceptions from observers to prevent
                # one observer from breaking the notification chain
                pass
