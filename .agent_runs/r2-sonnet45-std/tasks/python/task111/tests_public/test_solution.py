import itertools

import pytest
from src.solution import chunked


def test_exact_fit():
    assert list(chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]


def test_size_one():
    assert list(chunked([1, 2, 3], 1)) == [[1], [2], [3]]


def test_invalid_size():
    with pytest.raises(ValueError):
        list(chunked([1, 2, 3], 0))


def test_lazy_on_infinite_source():
    # An eager implementation would hang consuming the infinite source.
    gen = chunked(itertools.count(0), 3)
    assert next(gen) == [0, 1, 2]
    assert next(gen) == [3, 4, 5]
    assert next(gen) == [6, 7, 8]
