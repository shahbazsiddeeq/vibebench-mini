from src.solution import natural_sort


def test_numeric_parts():
    xs = ["file1", "file10", "file2"]
    assert natural_sort(xs) == ["file1", "file2", "file10"]


def test_mixed_case_and_prefix():
    xs = ["A2", "a11", "a1b", "a1a"]
    assert natural_sort(xs) == ["A2", "a1a", "a1b", "a11"]
