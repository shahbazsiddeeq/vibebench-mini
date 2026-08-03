class Observer:
    """Base class for observers in the Observer pattern."""
    
    def update(self, event, data):
        """
        Called when the subject notifies observers of an event.
        
        Args:
            event: The event name/type
            data: Optional data associated with the event
        """
        raise NotImplementedError("Subclasses must implement update()")


class Subject:
    """Subject class that manages observers and notifies them of events."""
    
    def __init__(self):
        """Initialize the subject with an empty list of observers."""
        self._observers = []
    
    def attach(self, observer):
        """
        Attach an observer to this subject.
        
        Args:
            observer: An Observer instance to attach
        """
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
            event: The event name/type
            data: Optional data to pass to observers (default: None)
        """
        for observer in self._observers:
            observer.update(event, data)
