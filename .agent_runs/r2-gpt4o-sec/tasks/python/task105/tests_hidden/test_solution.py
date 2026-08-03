import pytest

from src.solution import produce_consume


def test_basic_preserves_order():
    result = produce_consume([1, 2, 3, 4], lambda x: x * 2)
    assert result == [2, 4, 6, 8]


def test_single_worker():
    result = produce_consume([10, 20, 30], lambda x: x * 3, n_workers=1)
    assert result == [30, 60, 90]


def test_none_items_not_confused_with_sentinel():
    # None values must survive round-trip and not terminate a worker early.
    result = produce_consume([None, 1, None, 2], lambda x: x, n_workers=3)
    assert result == [None, 1, None, 2]


def test_invalid_workers_raises():
    with pytest.raises(ValueError):
        produce_consume([1, 2], lambda x: x, n_workers=0)
