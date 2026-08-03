from src.solution import power_set


def test_two_elements_exact():
    assert power_set([1, 2]) == [
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
    ]


def test_empty():
    assert power_set([]) == [frozenset()]


def test_duplicates_deduplicated():
    assert power_set([1, 1]) == [frozenset(), frozenset({1})]
    assert power_set([1, 1, 2]) == [
        frozenset(),
        frozenset({1}),
        frozenset({2}),
        frozenset({1, 2}),
    ]
