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


def test_detach():
    s = Subject()
    o = RecordingObserver()
    s.attach(o)
    s.detach(o)
    s.notify("click", 1)
    assert o.events == []


def test_multiple_observers():
    s = Subject()
    o1 = RecordingObserver()
    o2 = RecordingObserver()
    s.attach(o1)
    s.attach(o2)
    s.notify("evt", "data")
    assert o1.events == [("evt", "data")]
    assert o2.events == [("evt", "data")]


def test_no_observers():
    s = Subject()
    s.notify("evt", None)  # should not raise


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
    # The task description does not specify a notification order, so this test
    # requires only that every attached observer is notified exactly once.
    assert sorted(log) == ["a", "b", "c"]


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
