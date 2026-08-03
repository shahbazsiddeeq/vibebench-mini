from src.solution import find_replace


def test_no_match():
    assert find_replace("hello", {"world": "earth"}) == "hello"


def test_longer_key_wins():
    assert find_replace("hello", {"hell": "X", "hello": "Y"}) == "Y"


def test_multiple_occurrences():
    assert find_replace("aaa", {"a": "b"}) == "bbb"


def test_simultaneous_no_chaining():
    # Sequential application would turn 'a'->'b' then that 'b' (and the
    # original 'b') ->'c', giving 'cc'. Simultaneous must give 'bc'.
    assert find_replace("ab", {"a": "b", "b": "c"}) == "bc"
