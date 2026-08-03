from src.solution import find_anagram_pairs


def test_basic():
    result = find_anagram_pairs(["eat", "tea", "hello"])
    assert result == [("eat", "tea")]


def test_empty():
    assert find_anagram_pairs([]) == []


def test_multiple_pairs():
    result = find_anagram_pairs(["eat", "tea", "tan", "nat"])
    assert ("eat", "tea") in result
    assert ("nat", "tan") in result


def test_different_lengths_not_paired():
    assert find_anagram_pairs(["ab", "abc"]) == []


def test_full_output_order():
    result = find_anagram_pairs(["tea", "eat", "ate", "bat", "tab"])
    assert result == [
        ("ate", "eat"),
        ("ate", "tea"),
        ("bat", "tab"),
        ("eat", "tea"),
    ]
