import pytest

from src.solution import find_bare_excepts


def test_named_exceptions_not_reported():
    src = (
        "try:\n"
        "    x()\n"
        "except (ValueError, KeyError):\n"
        "    pass\n"
        "except OSError as e:\n"
        "    raise\n"
    )
    assert find_bare_excepts(src) == []


def test_bare_except_nested_in_function_and_loop():
    src = (
        "def f(items):\n"
        "    for it in items:\n"
        "        try:\n"
        "            use(it)\n"
        "        except:\n"
        "            continue\n"
    )
    assert find_bare_excepts(src) == [5]


def test_no_try_blocks():
    assert find_bare_excepts("x = 1\ny = 2\n") == []


def test_invalid_source_raises():
    with pytest.raises(ValueError):
        find_bare_excepts("try:\nexcept:\n")
