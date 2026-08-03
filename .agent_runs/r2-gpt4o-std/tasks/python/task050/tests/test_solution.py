from src.solution import unique_char_count


def test_some_duplicates():
    result = unique_char_count("aabbcd")
    assert result == {"c": 1, "d": 1}


def test_all_unique():
    result = unique_char_count("abc")
    assert result == {"a": 1, "b": 1, "c": 1}


def test_all_duplicates():
    assert unique_char_count("aabb") == {}


def test_empty():
    assert unique_char_count("") == {}


def test_single_char():
    assert unique_char_count("a") == {"a": 1}


def test_mixed():
    result = unique_char_count("abcabc")
    assert result == {}


def test_unique_chars_in_hello():
    result = unique_char_count("hello")
    assert set(result.keys()) == {"h", "e", "o"}  # 'l' appears twice


def test_first_appearance_order():
    # Keys must follow first-appearance order, not sorted or set order.
    result = unique_char_count("dbca")
    assert list(result.keys()) == ["d", "b", "c", "a"]


def test_order_with_duplicates_removed():
    result = unique_char_count("xxaybzy")
    assert list(result.items()) == [("a", 1), ("b", 1), ("z", 1)]
