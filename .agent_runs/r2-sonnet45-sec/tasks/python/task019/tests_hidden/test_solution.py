import pytest
from src.solution import MinStack




















class _Comparisons:
    count = 0


class _CInt:
    """Integer wrapper that counts every ordering comparison it takes part in."""

    __slots__ = ("v",)

    def __init__(self, v):
        self.v = v

    def __lt__(self, o):
        _Comparisons.count += 1
        return self.v < o.v

    def __le__(self, o):
        _Comparisons.count += 1
        return self.v <= o.v

    def __gt__(self, o):
        _Comparisons.count += 1
        return self.v > o.v

    def __ge__(self, o):
        _Comparisons.count += 1
        return self.v >= o.v

    def __eq__(self, o):
        return isinstance(o, _CInt) and self.v == o.v

    def __hash__(self):
        return hash(self.v)


def test_push_pop():
    s = MinStack()
    s.push(5)
    assert s.pop() == 5


def test_get_min_basic():
    s = MinStack()
    s.push(3)
    s.push(1)
    s.push(2)
    assert s.get_min() == 1


def test_pop_empty_raises():
    s = MinStack()
    with pytest.raises(IndexError):
        s.pop()


def test_get_min_empty_raises():
    s = MinStack()
    with pytest.raises(IndexError):
        s.get_min()


def test_empty_then_push():
    # Drain the stack to empty, confirm it raises, then reuse it.
    s = MinStack()
    s.push(5)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 5
    with pytest.raises(IndexError):
        s.get_min()
    with pytest.raises(IndexError):
        s.top()
    s.push(10)
    assert s.get_min() == 10
    assert s.top() == 10
    s.push(4)
    assert s.get_min() == 4
    s.push(20)
    assert s.get_min() == 4
