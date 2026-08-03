from src.solution import docstring_coverage
import pytest
import textwrap


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


def test_no_definitions_returns_one():
    assert docstring_coverage("x = 1\ny = 2\n") == 1.0


def test_empty_source():
    assert docstring_coverage("") == 1.0
