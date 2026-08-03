from src.solution import find_anagram_pairs


def test_no_anagrams():
    assert find_anagram_pairs(["abc", "def"]) == []


def test_single_word():
    assert find_anagram_pairs(["hello"]) == []


def test_lexicographic_order():
    pairs = find_anagram_pairs(["tea", "eat"])
    assert pairs == [("eat", "tea")]


def test_duplicate_words_not_self_paired():
    # A duplicate must not produce ("eat", "eat"); only the real pair remains.
    assert find_anagram_pairs(["eat", "eat", "tea"]) == [("eat", "tea")]


def test_case_sensitive():
    assert find_anagram_pairs(["Tea", "eat"]) == []
