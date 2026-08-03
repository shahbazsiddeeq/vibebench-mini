import collections

class Observer:
    """
    Base class for observers in the Observer pattern.
    Observers must implement the update method.
    """
    def update(self, event, data=None):
        """
        Receives updates from a Subject.

        Args:
            event (str): The type of event that occurred.
            data (any, optional): Additional data related to the event. Defaults to None.
        """
        raise NotImplementedError("Observers must implement the update method.")


class Subject:
    """
    Manages a list of observers and notifies them of changes.
    """
    def __init__(self):
        """
        Initializes a new Subject instance with an empty list of observers.
        """
        self._observers = []

    def attach(self, observer):
        """
        Attaches an observer to the subject.

        Args:
            observer (Observer): The observer to attach.

        Raises:
            TypeError: If the observer is not an instance of Observer.
            ValueError: If the observer is already attached.
        """
        if not isinstance(observer, Observer):
            raise TypeError("Observer must be an instance of the Observer class.")
        if observer in self._observers:
            raise ValueError("Observer is already attached.")
        self._observers.append(observer)

    def detach(self, observer):
        """
        Detaches an observer from the subject.

        Args:
            observer (Observer): The observer to detach.

        Raises:
            TypeError: If the observer is not an instance of Observer.
            ValueError: If the observer is not attached.
        """
        if not isinstance(observer, Observer):
            raise TypeError("Observer must be an instance of the Observer class.")
        try:
            self._observers.remove(observer)
        except ValueError:
            raise ValueError("Observer is not attached to this subject.")

    def notify(self, event, data=None):
        """
        Notifies all attached observers about an event.

        Args:
            event (str): The type of event that occurred. Must be a string.
            data (any, optional): Additional data related to the event. Defaults to None.

        Raises:
            TypeError: If the event is not a string.
        """
        if not isinstance(event, str):
            raise TypeError("Event must be a string.")

        # Iterate over a copy of the list to safely handle observers detaching themselves
        # during the notification process.
        for observer in list(self._observers):
            try:
                observer.update(event, data)
            except Exception as e:
                # Log the error or handle it appropriately without exposing internal details.
                # For this problem, we'll just let it pass, but in a real system,
                # you'd want to log this.
                pass
