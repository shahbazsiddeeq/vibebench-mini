from src.solution import TrafficLight

import pytest


def test_starts_green():
    assert TrafficLight().state == "green"


def test_next_returns_new_state_and_updates_property():
    t = TrafficLight()
    result = t.next()
    assert result == "yellow"
    assert t.state == "yellow"


def test_steps_multiple_wraps():
    t = TrafficLight()
    assert t.next(4) == "yellow"


def test_non_integer_steps_raises():
    t = TrafficLight()
    with pytest.raises(ValueError):
        t.next(1.5)


def test_large_steps_wrap_full_cycle():
    t = TrafficLight()
    # 3 == one full cycle, so 6 steps returns to green.
    assert t.next(6) == "green"
    assert t.next(7) == "yellow"
