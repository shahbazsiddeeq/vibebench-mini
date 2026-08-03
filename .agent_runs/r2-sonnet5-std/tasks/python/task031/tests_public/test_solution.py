from src.solution import flatten


def test_one_level():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_mixed_depth():
    assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


def test_empty_nested():
    assert flatten([[], [1], []]) == [1]


def test_deeply_nested_empty():
    assert flatten([[[]]]) == []
