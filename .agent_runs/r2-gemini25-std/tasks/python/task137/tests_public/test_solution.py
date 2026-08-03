from src.solution import find_markers
import pytest
import textwrap


def test_fixme():
    assert find_markers("# FIXME broken\n") == [(1, "FIXME")]


def test_multiple_lines_ordered():
    source = textwrap.dedent(
        """
        a = 1  # TODO one
        b = 2
        c = 3  # FIXME two
        """
    )
    assert find_markers(source) == [(2, "TODO"), (4, "FIXME")]


def test_marker_in_string_with_hash_in_untokenizable_source():
    # The '#' and 'TODO' both live inside a string literal, and the unclosed
    # bracket makes the source impossible to fully tokenize. A raw-text fallback
    # would wrongly report (2, 'TODO'); the correct result is [].
    source = 'data = [\n    "x = 1  # TODO",\n'
    assert find_markers(source) == []


def test_case_sensitive():
    assert find_markers("# todo lowercase ignored\n") == []
