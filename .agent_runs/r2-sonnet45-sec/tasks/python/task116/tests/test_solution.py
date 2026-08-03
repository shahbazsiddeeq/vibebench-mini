from src.solution import power_set


def test_two_elements_exact():
    assert power_set([1, 2]) == [
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
    ]


def test_three_elements_exact():
    assert power_set([1, 2, 3]) == [
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({3}),
        frozenset({1, 2}),
        frozenset({1, 3}),
        frozenset({2, 3}),
        frozenset({1, 2, 3}),
    ]


def test_empty():
    assert power_set([]) == [frozenset()]


def test_single():
    assert power_set([5]) == [frozenset(), frozenset({5})]


def test_duplicates_deduplicated():
    assert power_set([1, 1]) == [frozenset(), frozenset({1})]
    assert power_set([1, 1, 2]) == [
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
    ]


def test_sorted_by_size_then_elements():
    result = power_set([3, 1, 2])
    sizes = [len(s) for s in result]
    assert sizes == sorted(sizes)
    assert result[0] == frozenset()
    assert result[1:4] == [frozenset({1}), frozenset({2}), frozenset({3})]
