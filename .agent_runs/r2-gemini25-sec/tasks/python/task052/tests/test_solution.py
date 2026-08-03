from src.solution import find_anagram_pairs


def test_basic():
    result = find_anagram_pairs(["eat", "tea", "hello"])
    assert result == [("eat", "tea")]


def test_no_anagrams():
    assert find_anagram_pairs(["abc", "def"]) == []


def test_empty():
    assert find_anagram_pairs([]) == []


def test_single_word():
    assert find_anagram_pairs(["hello"]) == []


def test_multiple_pairs():
    result = find_anagram_pairs(["eat", "tea", "tan", "nat"])
    assert ("eat", "tea") in result
    assert ("nat", "tan") in result


def test_lexicographic_order():
    pairs = find_anagram_pairs(["tea", "eat"])
    assert pairs == [("eat", "tea")]


def test_different_lengths_not_paired():
    assert find_anagram_pairs(["ab", "abc"]) == []


def test_duplicate_words_not_self_paired():
    # A duplicate must not produce ("eat", "eat"); only the real pair remains.
    assert find_anagram_pairs(["eat", "eat", "tea"]) == [("eat", "tea")]


def test_full_output_order():
    result = find_anagram_pairs(["tea", "eat", "ate", "bat", "tab"])
    assert result == [
        ("ate", "eat"),
        ("ate", "tea"),
        ("bat", "tab"),
        ("eat", "tea"),
    ]


def test_case_sensitive():
    assert find_anagram_pairs(["Tea", "eat"]) == []
