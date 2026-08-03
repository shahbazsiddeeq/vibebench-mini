from src.solution import natural_sort


def test_numeric_value_not_lexicographic():
    # Pure lexicographic order would put "2" after "10"; numeric order must not.
    xs = ["item100", "item9", "item20", "item3"]
    assert natural_sort(xs) == ["item3", "item9", "item20", "item100"]


def test_mixed_numeric_and_text_no_crash():
    # A digit run and a letter run at the same position must not raise.
    xs = ["a1", "1a", "b"]
    assert natural_sort(xs) == ["1a", "a1", "b"]


def test_leading_number():
    xs = ["10th", "2nd", "1st"]
    assert natural_sort(xs) == ["1st", "2nd", "10th"]


def test_empty():
    assert natural_sort([]) == []
