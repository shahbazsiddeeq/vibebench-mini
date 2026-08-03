from src.solution import Handler, LowHandler, MidHandler, HighHandler

import pytest


def _full_chain() -> Handler:
    low = LowHandler()
    mid = MidHandler()
    high = HighHandler()
    low.set_next(mid).set_next(high)
    return low


def test_handle_low():
    assert _full_chain().handle(50) == "low"


def test_boundary_values():
    chain = _full_chain()
    assert chain.handle(99) == "low"
    assert chain.handle(100) == "mid"
    assert chain.handle(999) == "mid"
    assert chain.handle(1000) == "high"


def test_set_next_returns_next():
    low = LowHandler()
    mid = MidHandler()
    assert low.set_next(mid) is mid


def test_float_amount_raises():
    with pytest.raises(ValueError):
        _full_chain().handle(500.0)


def test_intermediate_handler_alone_delegates_to_none():
    mid = MidHandler()
    assert mid.handle(500) == "mid"
    assert mid.handle(50) is None
    assert mid.handle(5000) is None
