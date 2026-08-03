from src.solution import Observer, Subject


class RecordingObserver(Observer):
    def __init__(self):
        self.events = []

    def update(self, event, data):
        self.events.append((event, data))


def test_detach():
    s = Subject()
    o = RecordingObserver()
    s.attach(o)
    s.detach(o)
    s.notify("click", 1)
    assert o.events == []


def test_no_observers():
    s = Subject()
    s.notify("evt", None)  # should not raise


def test_subjects_are_independent():
    s1 = Subject()
    s2 = Subject()
    o1 = RecordingObserver()
    o2 = RecordingObserver()
    s1.attach(o1)
    s2.attach(o2)
    s1.notify("evt", 1)
    # o2 belongs only to s2, so it must not receive s1's notification
    assert o1.events == [("evt", 1)]
    assert o2.events == []
