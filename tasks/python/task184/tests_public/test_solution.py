import pytest

from src.solution import Peekable


def test_is_its_own_iterator():
    p = Peekable([1, 2])
    assert iter(p) is p


def test_empty_iterable():
    p = Peekable([])
    assert p.has_next() is False
    with pytest.raises(StopIteration):
        p.peek()
    with pytest.raises(StopIteration):
        next(p)


def test_interleaved_peek_and_next_no_skips():
    p = Peekable(range(5))
    seen = []
    while p.has_next():
        assert p.peek() == p.peek()  # stable look-ahead
        seen.append(next(p))
    assert seen == [0, 1, 2, 3, 4]


def test_peek_no_default_raises_at_end():
    p = Peekable([1])
    next(p)
    with pytest.raises(StopIteration):
        p.peek()


def test_non_iterable_raises_type_error():
    with pytest.raises(TypeError):
        Peekable(42)
    with pytest.raises(TypeError):
        Peekable(None)
