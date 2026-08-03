from src.solution import unique_char_count


def test_all_unique():
    result = unique_char_count("abc")
    assert result == {"a": 1, "b": 1, "c": 1}


def test_empty():
    assert unique_char_count("") == {}


def test_mixed():
    result = unique_char_count("abcabc")
    assert result == {}


def test_first_appearance_order():
    # Keys must follow first-appearance order, not sorted or set order.
    result = unique_char_count("dbca")
    assert list(result.keys()) == ["d", "b", "c", "a"]
