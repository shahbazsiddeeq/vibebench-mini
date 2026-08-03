# src/solution.py

class Observer:
    def update(self, event, data):
        raise NotImplementedError("Subclasses must implement this method.")


class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        if not isinstance(observer, Observer):
            raise ValueError("Observer must be an instance of Observer.")
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, event, data=None):
        if not isinstance(event, str):
            raise ValueError("Event must be a string.")
        for observer in self._observers:
            observer.update(event, data)
