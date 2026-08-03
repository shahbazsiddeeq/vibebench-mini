import pytest

from src.solution import cosine_similarity


def test_parallel_vectors():
    assert cosine_similarity([1, 2, 3], [2, 4, 6]) == 1.0


def test_worked_example_irrational():
    assert cosine_similarity([1, 1], [1, 0]) == 0.707107


def test_returns_float():
    assert isinstance(cosine_similarity([1, 2], [3, 4]), float)


def test_negatives():
    assert cosine_similarity([1, -1], [-1, 1]) == -1.0


def test_empty_raises():
    with pytest.raises(ValueError):
        cosine_similarity([], [])


def test_normalization_enforced():
    # dot([1,1],[1,0]) == 1, but the answer must be divided by the norms,
    # yielding 0.707107, not 1. A missing-normalization impl fails here.
    assert cosine_similarity([1, 1], [1, 0]) != 1.0
    assert cosine_similarity([1, 1], [1, 0]) == 0.707107
