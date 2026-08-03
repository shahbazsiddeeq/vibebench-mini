from src.solution import Observer, Subject


class RecordingObserver(Observer):
    def __init__(self):
        self.events = []

    def update(self, event, data):
        self.events.append((event, data))


def test_attach_and_notify():
    s = Subject()
    o = RecordingObserver()
    s.attach(o)
    s.notify("click", 42)
    assert o.events == [("click", 42)]


def test_multiple_observers():
    s = Subject()
    o1 = RecordingObserver()
    o2 = RecordingObserver()
    s.attach(o1)
    s.attach(o2)
    s.notify("evt", "data")
    assert o1.events == [("evt", "data")]
    assert o2.events == [("evt", "data")]


def test_notify_order():
    s = Subject()
    log = []

    class Ordered(Observer):
        def __init__(self, name):
            self.name = name

        def update(self, event, data):
            log.append(self.name)

    s.attach(Ordered("a"))
    s.attach(Ordered("b"))
    s.attach(Ordered("c"))
    s.notify("evt")
    assert log == ["a", "b", "c"]
