import pytest

from src.solution import cosine_similarity


def test_orthogonal_vectors():
    assert cosine_similarity([1, 0], [0, 1]) == 0.0


def test_opposite_vectors():
    assert cosine_similarity([1, 2], [-1, -2]) == -1.0


def test_single_element():
    assert cosine_similarity([3], [4]) == 1.0


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        cosine_similarity([1, 2, 3], [1, 2])


def test_zero_vector_raises():
    with pytest.raises(ValueError):
        cosine_similarity([0, 0], [1, 2])
