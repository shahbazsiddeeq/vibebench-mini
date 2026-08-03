"""Utilities for locating TODO and FIXME markers in Python comments."""

from __future__ import annotations

import io
import tokenize


def find_markers(source: str) -> list[tuple[int, str]]:
    """Return line numbers and markers found in actual Python comments.

    Tokenization stops at the first tokenization error. Comments emitted before
    that error are retained.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    results: list[tuple[int, str]] = []
    reported_lines: set[int] = set()
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)

    try:
        for token in tokens:
            if token.type == tokenize.ERRORTOKEN:
                break
            if token.type != tokenize.COMMENT:
                continue

            line_number = token.start[0]
            if line_number in reported_lines:
                continue

            comment = token.string
            todo_index = comment.find("TODO")
            fixme_index = comment.find("FIXME")

            if todo_index < 0 and fixme_index < 0:
                continue
            if todo_index >= 0 and (fixme_index < 0 or todo_index < fixme_index):
                marker = "TODO"
            else:
                marker = "FIXME"

            results.append((line_number, marker))
            reported_lines.add(line_number)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass

    return results
