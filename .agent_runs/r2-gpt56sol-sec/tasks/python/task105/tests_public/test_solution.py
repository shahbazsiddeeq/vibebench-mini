import pytest

from src.solution import produce_consume


def test_empty():
    assert produce_consume([], lambda x: x) == []


def test_string_items_order():
    result = produce_consume(["a", "b", "c"], lambda x: x.upper() + "!", n_workers=2)
    assert result == ["A!", "B!", "C!"]


def test_order_preserved_with_variable_work():
    import time

    def fn(x):
        # Later items finish sooner; output order must still match input.
        time.sleep(0.001 * ((5 - x) % 3))
        return x * 10

    items = list(range(6))
    assert produce_consume(items, fn, n_workers=4) == [x * 10 for x in items]
