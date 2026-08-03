from src.solution import find_replace


def test_basic():
    assert find_replace("hello world", {"hello": "hi", "world": "earth"}) == "hi earth"


def test_empty_replacements():
    assert find_replace("hello world", {}) == "hello world"


def test_partial_match():
    assert find_replace("foobar", {"foo": "baz"}) == "bazbar"


def test_empty_text():
    assert find_replace("", {"a": "b"}) == ""


def test_swap_no_chaining():
    # A true swap: sequential replacement would collapse both to one value.
    assert find_replace("aabb", {"a": "b", "b": "a"}) == "bbaa"
