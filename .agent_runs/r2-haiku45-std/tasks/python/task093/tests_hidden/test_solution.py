from src.solution import EventBus


def test_subscribe_publish():
    bus = EventBus()
    received = []
    bus.subscribe("click", lambda d: received.append(d))
    bus.publish("click", {"x": 5})
    assert received == [{"x": 5}]


def test_unsubscribe():
    bus = EventBus()
    calls = []

    def handler(d):
        calls.append(d)

    bus.subscribe("e", handler)
    bus.unsubscribe("e", handler)
    bus.publish("e", "data")
    assert calls == []


def test_data_passed():
    bus = EventBus()
    received = []
    bus.subscribe("evt", lambda d: received.append(d))
    bus.publish("evt", 42)
    assert received[0] == 42


def test_unsubscribe_during_publish_is_safe():
    # A handler that unsubscribes another (or itself) mid-publish must not
    # corrupt the ongoing dispatch: every handler present at publish time is
    # still invoked exactly once for this event.
    bus = EventBus()
    calls = []

    def second(d):
        calls.append("second")

    def first(d):
        calls.append("first")
        bus.unsubscribe("e", second)  # remove a not-yet-called handler

    bus.subscribe("e", first)
    bus.subscribe("e", second)

    bus.publish("e", None)
    # Both handlers registered at publish time run this round.
    assert calls == ["first", "second"]

    # The unsubscribe takes effect on the next publish.
    calls.clear()
    bus.publish("e", None)
    assert calls == ["first"]
