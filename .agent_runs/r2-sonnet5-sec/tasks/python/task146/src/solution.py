"""
Glob-style wildcard matching.

This module exposes a single public function, ``wildcard_match``, which
performs fully-anchored wildcard matching supporting ``*`` (match any run
of zero or more characters) and ``?`` (match exactly one character).

The implementation is deliberately defensive:
    * It never uses ``eval``/``exec`` or any dynamic code execution.
    * It validates input types and never raises for ordinary ``str``
      inputs; malformed (non-``str``) inputs simply yield ``False``
      instead of raising, so callers cannot trigger unexpected
      exceptions that might leak internal state.
    * It operates purely on Unicode code points via normal Python
      string indexing, with no external I/O or randomness involved.
"""

from __future__ import annotations

__all__ = ["wildcard_match"]


def wildcard_match(pattern: str, text: str) -> bool:
    """Return True if *pattern* fully matches *text*.

    ``*`` matches any run of zero or more characters (including none),
    ``?`` matches exactly one character. Matching is anchored at both
    ends (the whole ``text`` must be consumed) and is case-sensitive.

    This function never raises for ordinary string inputs; if the
    inputs are not both ``str`` instances, it safely returns ``False``
    rather than propagating a ``TypeError`` or similar exception.
    """
    # Defensive type validation: only accept str inputs. Do not raise;
    # simply report no match for anything unexpected. This avoids
    # leaking internal error details to callers.
    if not isinstance(pattern, str) or not isinstance(text, str):
        return False

    n, m = len(pattern), len(text)

    # dp[j] represents whether pattern[:i] matches text[:j] for the
    # current row i (rolling array to keep memory O(m)).
    # Initialize for i = 0 (empty pattern): matches only empty text.
    dp = [False] * (m + 1)
    dp[0] = True

    for i in range(1, n + 1):
        p_char = pattern[i - 1]
        new_dp = [False] * (m + 1)
        if p_char == "*":
            # '*' can match empty string, so it inherits from dp[0]
            # (previous row's zero-length match), and it also extends
            # matches from the current row's previous column.
            new_dp[0] = dp[0]
            for j in range(1, m + 1):
                new_dp[j] = new_dp[j - 1] or dp[j]
        elif p_char == "?":
            for j in range(1, m + 1):
                new_dp[j] = dp[j - 1]
            new_dp[0] = False
        else:
            for j in range(1, m + 1):
                new_dp[j] = dp[j - 1] and (text[j - 1] == p_char)
            new_dp[0] = False
        dp = new_dp

    return bool(dp[m])
