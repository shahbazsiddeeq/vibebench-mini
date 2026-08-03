from src.solution import non_snake_case_functions
import pytest
import textwrap


def test_all_snake_case():
    source = "def a():\n    pass\ndef b_c():\n    pass\n"
    assert non_snake_case_functions(source) == []


def test_async_function():
    source = "async def FetchData():\n    pass\n"
    assert non_snake_case_functions(source) == ["FetchData"]


def test_source_order_preserved():
    source = textwrap.dedent(
        """
        def Zeta():
            pass
        def alpha():
            pass
        def Beta():
            pass
        """
    )
    assert non_snake_case_functions(source) == ["Zeta", "Beta"]


def test_dunder_methods_not_reported():
    source = textwrap.dedent(
        """
        class Box:
            def __init__(self):
                pass
            def __repr__(self):
                pass
            def __eq__(self, other):
                pass
        """
    )
    assert non_snake_case_functions(source) == []
