class Observer:
    def update(self, event, data):
        """
        Receives updates from a Subject.
        This method should be overridden by concrete observers.
        """
        raise NotImplementedError("Subclasses must implement the update method.")


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """
        Attaches an observer to the subject.
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Detaches an observer from the subject.
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass  # Observer not found, do nothing

    def notify(self, event, data=None):
        """
        Notifies all attached observers about an event.
        """
        # Iterate over a copy of the list to avoid issues if observers detach themselves during notification
        for observer in list(self._observers):
            observer.update(event, data)
