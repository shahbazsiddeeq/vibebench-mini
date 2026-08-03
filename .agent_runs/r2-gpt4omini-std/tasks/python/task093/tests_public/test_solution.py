from src.solution import EventBus


def test_multiple_handlers():
    bus = EventBus()
    calls = []
    bus.subscribe("e", lambda d: calls.append(1))
    bus.subscribe("e", lambda d: calls.append(2))
    bus.publish("e")
    assert len(calls) == 2


def test_no_handler_no_error():
    bus = EventBus()
    bus.publish("nonexistent", "data")


def test_handlers_called_in_subscription_order():
    bus = EventBus()
    order = []
    for i in range(5):
        bus.subscribe("e", lambda d, i=i: order.append(i))
    bus.publish("e")
    assert order == [0, 1, 2, 3, 4]


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
