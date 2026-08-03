"""Scan Python source code for TODO and FIXME comment markers."""

from __future__ import annotations

import io
import tokenize


def find_markers(source: str) -> list[tuple[int, str]]:
    """Return line numbers and markers found in Python comment tokens."""
    results: list[tuple[int, str]] = []
    seen_lines: set[int] = set()
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)

    try:
        for token in tokens:
            if token.type != tokenize.COMMENT:
                continue

            line_number = token.start[0]
            if line_number in seen_lines:
                continue

            positions = (
                (position, marker)
                for marker in ("TODO", "FIXME")
                if (position := token.string.find(marker)) != -1
            )
            first = min(positions, default=None)
            if first is not None:
                results.append((line_number, first[1]))
                seen_lines.add(line_number)
    except (tokenize.TokenError, IndentationError):
        pass

    return results
