class Observer:
    def update(self, event: str, data):
        pass


class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: str, data=None):
        for obs in list(self._observers):
            obs.update(event, data)
