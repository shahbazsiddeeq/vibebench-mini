# src/solution.py

class Observer:
    def update(self, event, data):
        raise NotImplementedError("Subclasses should implement this!")

class Subject:
    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        if not isinstance(observer, Observer):
            raise TypeError("Observer must be an instance of Observer")
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, event, data=None):
        for observer in self._observers:
            try:
                observer.update(event, data)
            except Exception:
                # Log the exception or handle it as needed
                pass
