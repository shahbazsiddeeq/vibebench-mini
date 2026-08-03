from src.solution import TrafficLight

import pytest


def test_cycle_order():
    t = TrafficLight()
    assert t.next() == "yellow"
    assert t.next() == "red"
    assert t.next() == "green"


def test_steps_zero_keeps_state():
    t = TrafficLight()
    assert t.next(0) == "green"
    assert t.state == "green"


def test_negative_steps_raises():
    t = TrafficLight()
    with pytest.raises(ValueError):
        t.next(-1)


def test_bool_steps_raises():
    t = TrafficLight()
    with pytest.raises(ValueError):
        t.next(True)


def test_invalid_steps_does_not_advance():
    t = TrafficLight()
    t.next()  # yellow
    with pytest.raises(ValueError):
        t.next(-1)
    assert t.state == "yellow"
