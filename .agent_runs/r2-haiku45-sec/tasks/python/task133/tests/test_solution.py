from src.solution import docstring_coverage
import pytest
import textwrap


def test_half_documented():
    source = textwrap.dedent(
        '''
        def a():
            """documented"""
            return 1

        def b():
            return 2
        '''
    )
    assert docstring_coverage(source) == 0.5


def test_all_documented():
    source = textwrap.dedent(
        '''
        def a():
            """doc"""
            return 1

        class C:
            """doc"""
            pass
        '''
    )
    assert docstring_coverage(source) == 1.0


def test_none_documented():
    source = "def a():\n    return 1\n"
    assert docstring_coverage(source) == 0.0


def test_no_definitions_returns_one():
    assert docstring_coverage("x = 1\ny = 2\n") == 1.0


def test_async_and_class_counted():
    source = textwrap.dedent(
        '''
        async def a():
            """doc"""
            return 1

        class C:
            def m(self):
                return 0
        '''
    )
    # 3 defs (async a, class C, method m); only a documented -> 1/3
    assert docstring_coverage(source) == pytest.approx(1 / 3)


def test_empty_source():
    assert docstring_coverage("") == 1.0


def test_syntax_error_raises():
    with pytest.raises(ValueError):
        docstring_coverage("def (:\n")
