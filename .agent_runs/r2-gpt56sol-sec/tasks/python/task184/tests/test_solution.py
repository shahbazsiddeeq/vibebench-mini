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


def test_is_its_own_iterator():
    p = Peekable([1, 2])
    assert iter(p) is p


def test_full_iteration():
    assert list(Peekable([1, 2, 3, 4])) == [1, 2, 3, 4]


def test_empty_iterable():
    p = Peekable([])
    assert p.has_next() is False
    with pytest.raises(StopIteration):
        p.peek()
    with pytest.raises(StopIteration):
        next(p)


def test_peek_is_idempotent():
    p = Peekable([10, 20])
    assert p.peek() == 10
    assert p.peek() == 10
    assert p.peek() == 10
    assert next(p) == 10
    assert next(p) == 20


def test_interleaved_peek_and_next_no_skips():
    p = Peekable(range(5))
    seen = []
    while p.has_next():
        assert p.peek() == p.peek()  # stable look-ahead
        seen.append(next(p))
    assert seen == [0, 1, 2, 3, 4]


def test_peek_default_when_exhausted():
    p = Peekable([1])
    assert next(p) == 1
    assert p.peek("done") == "done"
    # Default peek must not consume or corrupt state.
    assert p.has_next() is False


def test_peek_no_default_raises_at_end():
    p = Peekable([1])
    next(p)
    with pytest.raises(StopIteration):
        p.peek()


def test_works_with_generator():
    def gen():
        yield "a"
        yield "b"

    p = Peekable(gen())
    assert p.peek() == "a"
    assert list(p) == ["a", "b"]


def test_non_iterable_raises_type_error():
    with pytest.raises(TypeError):
        Peekable(42)
    with pytest.raises(TypeError):
        Peekable(None)
