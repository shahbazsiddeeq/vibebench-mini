from src.solution import Handler, LowHandler, MidHandler, HighHandler

import pytest


def _full_chain() -> Handler:
    low = LowHandler()
    mid = MidHandler()
    high = HighHandler()
    low.set_next(mid).set_next(high)
    return low


def test_handle_mid():
    assert _full_chain().handle(500) == "mid"


def test_handle_high():
    assert _full_chain().handle(5000) == "high"


def test_lone_low_handler_returns_none():
    assert LowHandler().handle(500) is None


def test_invalid_amount_raises():
    with pytest.raises(ValueError):
        _full_chain().handle("500")


def test_bool_amount_raises():
    # bool is a subclass of int but must not be accepted as an amount.
    with pytest.raises(ValueError):
        _full_chain().handle(True)


def test_partial_chain_returns_none_when_unhandled():
    # low -> mid only; a high amount has no handler and returns None.
    low = LowHandler()
    mid = MidHandler()
    low.set_next(mid)
    assert low.handle(5000) is None
    assert low.handle(500) == "mid"
    assert low.handle(5) == "low"
