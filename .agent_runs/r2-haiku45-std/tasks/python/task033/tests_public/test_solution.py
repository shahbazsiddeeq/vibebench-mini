from src.solution import group_anagrams


def test_all_different():
    result = group_anagrams(["abc", "def"])
    assert len(result) == 2


def test_empty_list():
    assert group_anagrams([]) == []


def test_groups_sorted_by_first():
    result = group_anagrams(["cat", "dog", "act"])
    first_elements = [g[0] for g in result]
    assert first_elements == sorted(first_elements)
