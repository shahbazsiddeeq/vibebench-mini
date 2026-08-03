from __future__ import annotations

import io
import tokenize


def _markers_from_comment(text: str) -> str | None:
    """Return the first-occurring marker ('TODO'/'FIXME') in ``text`` or None."""
    todo = text.find("TODO")
    fixme = text.find("FIXME")
    if todo == -1 and fixme == -1:
        return None
    if fixme == -1 or (todo != -1 and todo < fixme):
        return "TODO"
    return "FIXME"


def find_markers(source: str) -> list[tuple[int, str]]:
    """Return (line number, marker) pairs for TODO/FIXME markers in comments.

    Only markers appearing inside ``#`` comments are reported. If a line has
    both, the first occurring marker is used. Results are ordered by line.
    """
    results: dict[int, str] = {}
    tokens = tokenize.generate_tokens(io.StringIO(source).readline)
    try:
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                marker = _markers_from_comment(tok.string)
                if marker is not None:
                    line = tok.start[0]
                    if line not in results:
                        results[line] = marker
    except (tokenize.TokenError, IndentationError, SyntaxError):
        # The source could not be fully tokenized (e.g. an unclosed bracket or
        # string). We keep the COMMENT tokens produced before the failure and
        # stop; we do NOT fall back to a raw text scan, which would wrongly
        # report markers that live inside string literals.
        pass

    return [(line, results[line]) for line in sorted(results)]
