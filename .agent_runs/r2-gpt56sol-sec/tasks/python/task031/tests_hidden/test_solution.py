from src.solution import flatten


def test_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_deep_nesting():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_empty():
    assert flatten([]) == []


def test_mixed_types():
    assert flatten([1, "a", [2, "b"]]) == [1, "a", 2, "b"]
