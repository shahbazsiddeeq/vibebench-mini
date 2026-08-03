from src.solution import find_markers
import pytest
import textwrap


def test_basic_todo():
    assert find_markers("x = 1  # TODO fix\n") == [(1, "TODO")]


def test_fixme():
    assert find_markers("# FIXME broken\n") == [(1, "FIXME")]


def test_both_first_wins():
    assert find_markers("# FIXME then TODO\n") == [(1, "FIXME")]
    assert find_markers("# TODO then FIXME\n") == [(1, "TODO")]


def test_multiple_lines_ordered():
    source = textwrap.dedent(
        """
        a = 1  # TODO one
        b = 2
        c = 3  # FIXME two
        """
    )
    assert find_markers(source) == [(2, "TODO"), (4, "FIXME")]


def test_marker_in_string_not_reported():
    source = 's = "TODO not a comment"\n'
    assert find_markers(source) == []


def test_marker_in_string_with_hash_in_untokenizable_source():
    # The '#' and 'TODO' both live inside a string literal, and the unclosed
    # bracket makes the source impossible to fully tokenize. A raw-text fallback
    # would wrongly report (2, 'TODO'); the correct result is [].
    source = 'data = [\n    "x = 1  # TODO",\n'
    assert find_markers(source) == []


def test_comment_before_tokenize_failure_still_reported():
    # The real comment on line 1 is tokenized before the unclosed paren fails.
    source = "x = 1  # TODO keep\ny = (\n"
    assert find_markers(source) == [(1, "TODO")]


def test_case_sensitive():
    assert find_markers("# todo lowercase ignored\n") == []


def test_no_markers():
    assert find_markers("x = 1  # just a comment\n") == []
