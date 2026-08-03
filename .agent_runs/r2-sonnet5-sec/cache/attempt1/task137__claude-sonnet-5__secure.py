"""
TODO/FIXME Marker Scanner
=========================

This module exposes :func:`find_markers`, which scans Python source code
and reports every line whose *comment* token contains the literal
substring ``'TODO'`` or ``'FIXME'`` (case-sensitive).

Only text that the tokenizer recognizes as an actual comment token is
considered - markers appearing inside string literals are never reported.
If tokenization fails partway through the source (e.g. due to an unclosed
bracket or string), only the comments successfully tokenized *before* the
failure are reported; there is no raw-text fallback of any kind.
"""

from __future__ import annotations

import io
import tokenize
from typing import List, Tuple

__all__ = ["find_markers"]

_MARKERS = ("TODO", "FIXME")


def _first_marker(comment_text: str) -> str | None:
    """Return whichever marker occurs first (leftmost) in comment_text.

    Returns None if neither marker is present.
    """
    best_marker = None
    best_index = None
    for marker in _MARKERS:
        idx = comment_text.find(marker)
        if idx == -1:
            continue
        if best_index is None or idx < best_index:
            best_index = idx
            best_marker = marker
    return best_marker


def find_markers(source: str) -> List[Tuple[int, str]]:
    """Scan `source` for TODO/FIXME markers appearing in comments.

    Parameters
    ----------
    source:
        Python source code to scan. Must be a string.

    Returns
    -------
    List of (line_number, marker) tuples, one per line that contains a
    marker in an actual comment token, ordered by ascending line number.
    If the source fails to tokenize partway through, only comments seen
    before the failure point are included.
    """
    if not isinstance(source, str):
        raise TypeError("source must be a string")

    results: dict[int, str] = {}

    try:
        token_stream = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok in token_stream:
            if tok.type == tokenize.COMMENT:
                comment_string = tok.string
                # Comment tokens always start with '#'; strip it defensively.
                if comment_string.startswith("#"):
                    comment_text = comment_string[1:]
                else:
                    comment_text = comment_string

                marker = _first_marker(comment_text)
                if marker is not None:
                    line_no = tok.start[0]
                    # Only one result per line; first found wins (there
                    # should normally be at most one comment per line).
                    if line_no not in results:
                        results[line_no] = marker
    except (tokenize.TokenError, IndentationError, SyntaxError):
        # Tokenization failed partway through; keep whatever was
        # collected so far and do not attempt any raw-text fallback.
        pass
    except Exception:
        # Any other unexpected tokenizer error: fail safe, do not leak
        # internal details, keep partial results collected so far.
        pass

    return sorted(results.items())
