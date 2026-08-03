import pytest

from src.solution import find_duplicate_dict_keys


def test_worked_example():
    assert find_duplicate_dict_keys("d = {'a': 1, 'b': 2, 'a': 3}") == [(1, "a")]


def test_duplicate_reported_once_even_if_triple():
    assert find_duplicate_dict_keys("d = {1: 1, 1: 2, 1: 3}") == [(1, 1)]


def test_variable_keys_ignored():
    src = "k = 'a'\nd = {k: 1, k: 2}\n"
    assert find_duplicate_dict_keys(src) == []


def test_nested_dicts_each_analysed():
    src = "d = {'a': {'b': 1, 'b': 2}, 'a': 5}\n"
    # inner dup 'b' and outer dup 'a', both on line 1; sorted by repr(key)
    assert find_duplicate_dict_keys(src) == [(1, "a"), (1, "b")]


def test_mutation_killer_dict_inside_string():
    # A regex/text scanner might parse the dict written inside the string.
    src = (
        "s = \"{'a': 1, 'a': 2}\"\n"
        "real = {'a': 1, 'b': 2}\n"
    )
    assert find_duplicate_dict_keys(src) == []


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        find_duplicate_dict_keys("d = {'a': }\n")
