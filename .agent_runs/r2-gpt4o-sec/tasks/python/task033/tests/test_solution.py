from src.solution import group_anagrams


def test_basic():
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert result == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]


def test_all_different():
    result = group_anagrams(["abc", "def"])
    assert len(result) == 2


def test_all_same_anagram():
    result = group_anagrams(["abc", "bca", "cab"])
    assert len(result) == 1
    assert sorted(result[0]) == ["abc", "bca", "cab"]


def test_empty_list():
    assert group_anagrams([]) == []


def test_single_word():
    assert group_anagrams(["hello"]) == [["hello"]]


def test_groups_sorted_by_first():
    result = group_anagrams(["cat", "dog", "act"])
    first_elements = [g[0] for g in result]
    assert first_elements == sorted(first_elements)


def test_each_group_sorted():
    result = group_anagrams(["eat", "tea", "ate"])
    assert result[0] == ["ate", "eat", "tea"]
