import pytest

from src.solution import find_duplicate_dict_keys


def test_no_duplicates():
    assert find_duplicate_dict_keys("d = {'a': 1, 'b': 2, 'c': 3}") == []


def test_type_sensitive_no_false_positive():
    # 1 (int), 1.0 (float) and True (bool) are all distinct keys here.
    assert find_duplicate_dict_keys("d = {1: 'a', True: 'b', 1.0: 'c'}") == []


def test_unpacking_skipped():
    src = "base = {}\nd = {**base, 'k': 1, 'k': 2}\n"
    assert find_duplicate_dict_keys(src) == [(2, "k")]


def test_multiple_dicts_across_lines():
    src = (
        "x = {'p': 1, 'p': 2}\n"
        "y = {'q': 1}\n"
        "z = {3: 'a', 3: 'b'}\n"
    )
    assert find_duplicate_dict_keys(src) == [(1, "p"), (3, 3)]


def test_none_and_bool_keys():
    src = "d = {None: 1, None: 2, False: 3, False: 4}\n"
    # sorted by repr(key): repr(False)='False' < repr(None)='None'
    assert find_duplicate_dict_keys(src) == [(1, False), (1, None)]
