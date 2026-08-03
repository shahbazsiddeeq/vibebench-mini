import random

import pytest

from src.solution import kth_largest


def test_largest():
    assert kth_largest([3, 2, 1, 5, 6, 4], 1) == 6


def test_single_element():
    assert kth_largest([42], 1) == 42


def test_duplicates_mixed():
    assert kth_largest([1, 2, 2, 3], 2) == 2


def test_middle_value_mutation_killer():
    # 3rd largest of a known multiset.
    assert kth_largest([7, 10, 4, 3, 20, 15], 3) == 10


def test_k_too_large_raises():
    with pytest.raises(ValueError):
        kth_largest([1, 2, 3], 4)


def test_matches_sorted_on_random_inputs():
    rng = random.Random(1234)
    for _ in range(50):
        data = [rng.randint(-50, 50) for _ in range(rng.randint(1, 40))]
        expected = sorted(data, reverse=True)
        for k in range(1, len(data) + 1):
            assert kth_largest(data, k) == expected[k - 1]
