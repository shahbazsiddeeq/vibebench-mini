"""A simple implementation of the Observer design pattern."""


class Observer:
    """Base class for objects that receive subject notifications."""

    def update(self, event, data):
        """Handle a notification from a subject."""
        raise NotImplementedError("Observers must implement update()")


class Subject:
    """Maintains observers and broadcasts events to them."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Attach an observer, avoiding duplicate registrations."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Detach an observer if it is currently registered."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event, data=None):
        """Notify all currently attached observers."""
        for observer in tuple(self._observers):
            observer.update(event, data)
