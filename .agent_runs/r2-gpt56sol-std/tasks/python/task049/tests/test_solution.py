from src.solution import find_replace


def test_basic():
    assert find_replace("hello world", {"hello": "hi", "world": "earth"}) == "hi earth"


def test_no_match():
    assert find_replace("hello", {"world": "earth"}) == "hello"


def test_empty_replacements():
    assert find_replace("hello world", {}) == "hello world"


def test_longer_key_wins():
    assert find_replace("hello", {"hell": "X", "hello": "Y"}) == "Y"


def test_partial_match():
    assert find_replace("foobar", {"foo": "baz"}) == "bazbar"


def test_multiple_occurrences():
    assert find_replace("aaa", {"a": "b"}) == "bbb"


def test_empty_text():
    assert find_replace("", {"a": "b"}) == ""


def test_simultaneous_no_chaining():
    # Sequential application would turn 'a'->'b' then that 'b' (and the
    # original 'b') ->'c', giving 'cc'. Simultaneous must give 'bc'.
    assert find_replace("ab", {"a": "b", "b": "c"}) == "bc"


def test_swap_no_chaining():
    # A true swap: sequential replacement would collapse both to one value.
    assert find_replace("aabb", {"a": "b", "b": "a"}) == "bbaa"
