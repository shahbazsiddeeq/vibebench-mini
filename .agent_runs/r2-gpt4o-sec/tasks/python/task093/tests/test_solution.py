from src.solution import EventBus


def test_subscribe_publish():
    bus = EventBus()
    received = []
    bus.subscribe("click", lambda d: received.append(d))
    bus.publish("click", {"x": 5})
    assert received == [{"x": 5}]


def test_multiple_handlers():
    bus = EventBus()
    calls = []
    bus.subscribe("e", lambda d: calls.append(1))
    bus.subscribe("e", lambda d: calls.append(2))
    bus.publish("e")
    assert len(calls) == 2


def test_unsubscribe():
    bus = EventBus()
    calls = []

    def handler(d):
        calls.append(d)

    bus.subscribe("e", handler)
    bus.unsubscribe("e", handler)
    bus.publish("e", "data")
    assert calls == []


def test_no_handler_no_error():
    bus = EventBus()
    bus.publish("nonexistent", "data")


def test_data_passed():
    bus = EventBus()
    received = []
    bus.subscribe("evt", lambda d: received.append(d))
    bus.publish("evt", 42)
    assert received[0] == 42


def test_handlers_called_in_subscription_order():
    bus = EventBus()
    order = []
    for i in range(5):
        bus.subscribe("e", lambda d, i=i: order.append(i))
    bus.publish("e")
    assert order == [0, 1, 2, 3, 4]


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


def test_handler_unsubscribing_itself_during_publish():
    bus = EventBus()
    calls = []

    def once(d):
        calls.append(d)
        bus.unsubscribe("e", once)

    bus.subscribe("e", once)
    bus.publish("e", 1)
    bus.publish("e", 2)
    assert calls == [1]
