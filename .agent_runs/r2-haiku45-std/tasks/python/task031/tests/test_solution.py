from src.solution import flatten


def test_already_flat():
    assert flatten([1, 2, 3]) == [1, 2, 3]


def test_one_level():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_deep_nesting():
    assert flatten([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_mixed_depth():
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


def test_empty():
    assert flatten([]) == []


def test_empty_nested():
    assert flatten([[], [1], []]) == [1]


def test_mixed_types():
    assert flatten([1, "a", [2, "b"]]) == [1, "a", 2, "b"]


def test_deeply_nested_empty():
    assert flatten([[[]]]) == []
