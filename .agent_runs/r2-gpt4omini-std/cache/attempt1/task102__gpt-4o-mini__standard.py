# src/solution.py

class Observer:
    def update(self, event, data):
        raise NotImplementedError("Subclasses should implement this method.")


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event, data=None):
        for observer in self._observers:
            observer.update(event, data)
