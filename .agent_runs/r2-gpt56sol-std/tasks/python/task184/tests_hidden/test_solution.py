import pytest

from src.solution import Peekable


def test_worked_example():
    p = Peekable([1, 2, 3])
    assert p.peek() == 1
    assert next(p) == 1
    assert p.peek() == 2
    assert list(p) == [2, 3]
    assert p.has_next() is False
    assert p.peek(99) == 99


def test_full_iteration():
    assert list(Peekable([1, 2, 3, 4])) == [1, 2, 3, 4]


def test_peek_is_idempotent():
    p = Peekable([10, 20])
    assert p.peek() == 10
    assert p.peek() == 10
    assert p.peek() == 10
    assert next(p) == 10
    assert next(p) == 20


def test_peek_default_when_exhausted():
    p = Peekable([1])
    assert next(p) == 1
    assert p.peek("done") == "done"
    # Default peek must not consume or corrupt state.
    assert p.has_next() is False


def test_works_with_generator():
    def gen():
        yield "a"
        yield "b"

    p = Peekable(gen())
    assert p.peek() == "a"
    assert list(p) == ["a", "b"]
