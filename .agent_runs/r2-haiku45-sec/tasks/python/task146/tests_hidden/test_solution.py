from src.solution import wildcard_match


def test_worked_example_star_and_question():
    assert wildcard_match("a*c?", "abbcx") is True


def test_question_requires_a_character():
    assert wildcard_match("a?c", "ac") is False


def test_empty_pattern_rejects_nonempty():
    assert wildcard_match("", "x") is False


def test_single_star_matches_anything():
    assert wildcard_match("*", "anything at all") is True


def test_literal_mismatch():
    assert wildcard_match("hello", "hallo") is False


def test_question_matches_exactly_one():
    assert wildcard_match("h?llo", "hello") is True
    assert wildcard_match("h?llo", "heello") is False


def test_trailing_star_absorbs_rest():
    assert wildcard_match("abc*", "abcdef") is True
    assert wildcard_match("abc*", "abc") is True


def test_unicode_one_codepoint():
    assert wildcard_match("caf?", "café") is True
    assert wildcard_match("?", "☃") is True


def test_mutation_killer_greedy_backtrack():
    # A non-backtracking star (greedy without retry) would wrongly fail this.
    assert wildcard_match("a*a*a", "aXaXaXa") is True
    assert wildcard_match("a*a*b", "aXaXaXa") is False
