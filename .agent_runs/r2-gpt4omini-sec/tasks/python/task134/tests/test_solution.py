from src.solution import non_snake_case_functions
import pytest
import textwrap


def test_basic_mix():
    source = textwrap.dedent(
        """
        def myFunc():
            pass

        def good_name():
            pass

        def HTTPGet():
            pass
        """
    )
    assert non_snake_case_functions(source) == ["myFunc", "HTTPGet"]


def test_all_snake_case():
    source = "def a():\n    pass\ndef b_c():\n    pass\n"
    assert non_snake_case_functions(source) == []


def test_nested_functions_included():
    source = textwrap.dedent(
        """
        def outer():
            def innerBad():
                pass
            def inner_ok():
                pass
        """
    )
    assert non_snake_case_functions(source) == ["innerBad"]


def test_async_function():
    source = "async def FetchData():\n    pass\n"
    assert non_snake_case_functions(source) == ["FetchData"]


def test_leading_underscore_is_ok():
    source = "def _private():\n    pass\n"
    assert non_snake_case_functions(source) == []


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


def test_class_methods_are_checked_but_class_name_is_not():
    source = textwrap.dedent(
        """
        class CamelWidget:
            def __init__(self):
                pass

            def doThing(self):
                pass

            def run_task(self):
                pass

            async def FetchAll(self):
                pass
        """
    )
    # The CamelCase class name and the __init__ dunder are not reported;
    # camelCase / CamelCase methods are.
    assert non_snake_case_functions(source) == ["doThing", "FetchAll"]


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


def test_syntax_error_raises():
    with pytest.raises(ValueError):
        non_snake_case_functions("def (:\n")
