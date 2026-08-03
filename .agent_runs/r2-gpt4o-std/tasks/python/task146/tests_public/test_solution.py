from src.solution import wildcard_match


def test_star_prefix_extension():
    assert wildcard_match("*.txt", "file.txt") is True


def test_empty_pattern_matches_empty():
    assert wildcard_match("", "") is True


def test_single_star_matches_empty():
    assert wildcard_match("*", "") is True


def test_literal_full_match():
    assert wildcard_match("hello", "hello") is True


def test_anchored_not_substring():
    assert wildcard_match("cat", "concatenate") is False


def test_multiple_stars():
    assert wildcard_match("*a*b*", "xxaxxbxx") is True
    assert wildcard_match("*a*b*", "xxbxxaxx") is False


def test_case_sensitive():
    assert wildcard_match("File", "file") is False


def test_star_and_literal_interplay():
    assert wildcard_match("*b", "aaab") is True
    assert wildcard_match("*b", "aaabc") is False
