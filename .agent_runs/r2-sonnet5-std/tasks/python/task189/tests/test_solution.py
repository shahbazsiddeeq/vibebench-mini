import pytest

from src.solution import find_duplicate_dict_keys


def test_worked_example():
    assert find_duplicate_dict_keys("d = {'a': 1, 'b': 2, 'a': 3}") == [(1, "a")]


def test_no_duplicates():
    assert find_duplicate_dict_keys("d = {'a': 1, 'b': 2, 'c': 3}") == []


def test_duplicate_reported_once_even_if_triple():
    assert find_duplicate_dict_keys("d = {1: 1, 1: 2, 1: 3}") == [(1, 1)]


def test_type_sensitive_no_false_positive():
    # 1 (int), 1.0 (float) and True (bool) are all distinct keys here.
    assert find_duplicate_dict_keys("d = {1: 'a', True: 'b', 1.0: 'c'}") == []


def test_variable_keys_ignored():
    src = "k = 'a'\nd = {k: 1, k: 2}\n"
    assert find_duplicate_dict_keys(src) == []


def test_unpacking_skipped():
    src = "base = {}\nd = {**base, 'k': 1, 'k': 2}\n"
    assert find_duplicate_dict_keys(src) == [(2, "k")]


def test_nested_dicts_each_analysed():
    src = "d = {'a': {'b': 1, 'b': 2}, 'a': 5}\n"
    # inner dup 'b' and outer dup 'a', both on line 1; sorted by repr(key)
    assert find_duplicate_dict_keys(src) == [(1, "a"), (1, "b")]


def test_multiple_dicts_across_lines():
    src = (
        "x = {'p': 1, 'p': 2}\n"
        "y = {'q': 1}\n"
        "z = {3: 'a', 3: 'b'}\n"
    )
    assert find_duplicate_dict_keys(src) == [(1, "p"), (3, 3)]


def test_mutation_killer_dict_inside_string():
    # A regex/text scanner might parse the dict written inside the string.
    src = (
        "s = \"{'a': 1, 'a': 2}\"\n"
        "real = {'a': 1, 'b': 2}\n"
    )
    assert find_duplicate_dict_keys(src) == []


def test_none_and_bool_keys():
    src = "d = {None: 1, None: 2, False: 3, False: 4}\n"
    # sorted by repr(key): repr(False)='False' < repr(None)='None'
    assert find_duplicate_dict_keys(src) == [(1, False), (1, None)]


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        find_duplicate_dict_keys("d = {'a': }\n")
