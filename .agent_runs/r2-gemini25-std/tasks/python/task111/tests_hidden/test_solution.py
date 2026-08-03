import itertools

import pytest
from src.solution import chunked


def test_basic():
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_size_larger_than_data():
    assert list(chunked([1, 2], 5)) == [[1, 2]]


def test_empty():
    assert list(chunked([], 3)) == []


def test_generator_input():
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_yields_incrementally():
    # Each chunk must be produced before the whole source is consumed.
    def source():
        yield 1
        yield 2
        yield 3
        raise AssertionError("source consumed past the first chunk")

    gen = chunked(source(), 2)
    assert next(gen) == [1, 2]
