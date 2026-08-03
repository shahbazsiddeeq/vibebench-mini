from src.solution import natural_sort


def test_numeric_parts():
    xs = ["file1", "file10", "file2"]
    assert natural_sort(xs) == ["file1", "file2", "file10"]


def test_numeric_value_not_lexicographic():
    # Pure lexicographic order would put "2" after "10"; numeric order must not.
    xs = ["item100", "item9", "item20", "item3"]
    assert natural_sort(xs) == ["item3", "item9", "item20", "item100"]


def test_case_sensitive_uppercase_first():
    xs = ["A2", "a11", "a1b", "a1a"]
    assert natural_sort(xs) == ["A2", "a1a", "a1b", "a11"]


def test_mixed_numeric_and_text_no_crash():
    # A digit run and a letter run at the same position must not raise.
    xs = ["a1", "1a", "b"]
    assert natural_sort(xs) == ["1a", "a1", "b"]


def test_numeric_run_sorts_before_text_run():
    xs = ["x9", "x9y", "1", "z"]
    assert natural_sort(xs) == ["1", "x9", "x9y", "z"]


def test_leading_number():
    xs = ["10th", "2nd", "1st"]
    assert natural_sort(xs) == ["1st", "2nd", "10th"]


def test_returns_new_list_and_stable():
    original = ["file2", "file10", "file1"]
    snapshot = list(original)
    result = natural_sort(original)
    assert result is not original
    assert original == snapshot  # input untouched
    # equal keys keep their input order (stable)
    dups = ["file1", "file01", "file1"]
    assert natural_sort(dups) == ["file1", "file01", "file1"]


def test_empty():
    assert natural_sort([]) == []
