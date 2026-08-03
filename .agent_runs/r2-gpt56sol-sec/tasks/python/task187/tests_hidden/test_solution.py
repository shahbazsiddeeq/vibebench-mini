import pytest

from src.solution import find_bare_excepts


def test_worked_example():
    src = (
        "try:\n"
        "    risky()\n"
        "except ValueError:\n"
        "    pass\n"
        "except:\n"
        "    pass\n"
    )
    assert find_bare_excepts(src) == [5]


def test_multiple_bare_handlers_sorted():
    src = (
        "try:\n"
        "    a()\n"
        "except:\n"
        "    b()\n"
        "try:\n"
        "    c()\n"
        "except (A, B):\n"
        "    d()\n"
        "except:\n"
        "    e()\n"
    )
    assert find_bare_excepts(src) == [3, 9]


def test_mutation_killer_string_and_comment_ignored():
    # A regex/line scanner for a line that is 'except:' would flag these.
    src = (
        "s = 'except:'\n"
        "msg = \"handle except: gracefully\"\n"
        "# except:\n"
        "try:\n"
        "    work()\n"
        "except Exception:\n"
        "    pass\n"
    )
    assert find_bare_excepts(src) == []


def test_try_star_named_not_bare():
    # except* must always name a type, so it is never bare.
    src = (
        "try:\n"
        "    work()\n"
        "except* ValueError:\n"
        "    pass\n"
    )
    assert find_bare_excepts(src) == []
