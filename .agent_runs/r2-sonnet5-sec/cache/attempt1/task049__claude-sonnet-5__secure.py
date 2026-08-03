"""
src/solution.py

A secure, self-contained implementation of a simultaneous
find-and-replace utility.

The function `find_replace` takes a body of text and a mapping of
search strings to replacement strings, and performs all replacements
"simultaneously" -- meaning that replacement output is never re-scanned
for further matches, and overlapping keys are resolved by preferring
the longest matching key at each position.

Design notes (security & robustness):
    * No use of eval/exec or any dynamic code execution.
    * Strict input validation with clear, non-leaky error messages
      (no internal state, tracebacks, or sensitive data exposed).
    * Uses the `re` module with all user-supplied keys escaped via
      `re.escape` to avoid regex injection / unintended pattern
      behavior.
    * Uses only the Python standard library.
    * Deterministic behavior -- no randomness is required for this
      task, so `secrets` is not used here, but is noted as the
      preferred module for any future randomness needs.
"""

from __future__ import annotations

import re
from typing import Dict


def find_replace(text: str, replacements: Dict[str, str]) -> str:
    """
    Simultaneously replace all occurrences of keys in `replacements`
    found in `text` with their corresponding values.

    Rules:
        - All replacements happen "at once": the result of one
          replacement is never re-scanned for further matches.
        - If multiple keys could match at the same position (i.e.
          overlapping keys), the longest key wins.
        - Non-overlapping, non-matching text is left unchanged.

    Args:
        text: The input string to perform replacements on.
        replacements: A mapping from search strings (keys) to
            replacement strings (values). Keys must be non-empty
            strings; values must be strings.

    Returns:
        The resulting string after all simultaneous replacements.

    Raises:
        TypeError: If `text` is not a string, `replacements` is not a
            dict, or any key/value within `replacements` is not a
            string.
        ValueError: If any key in `replacements` is an empty string.
    """
    _validate_inputs(text, replacements)

    if not replacements:
        return text

    # Sort keys by length descending so that, when combined into a
    # single alternation pattern, the regex engine will prefer the
    # longest match at any given position (Python's `re` tries
    # alternatives in order and returns the first that matches,
    # so ordering matters for overlapping keys of different lengths).
    sorted_keys = sorted(replacements.keys(), key=len, reverse=True)

    # Escape each key to ensure it's treated as a literal string in
    # the regex, preventing regex injection via crafted keys.
    pattern = "|".join(re.escape(key) for key in sorted_keys)

    compiled = re.compile(pattern)

    def _replacement(match: "re.Match[str]") -> str:
        matched_text = match.group(0)
        # Direct dict lookup is safe because matched_text is guaranteed
        # to be one of the original keys (regex matched a literal key).
        return replacements[matched_text]

    return compiled.sub(_replacement, text)


def _validate_inputs(text: str, replacements: Dict[str, str]) -> None:
    """
    Validate the inputs to `find_replace`, raising appropriate,
    non-leaky exceptions on failure.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not isinstance(replacements, dict):
        raise TypeError("replacements must be a dictionary")

    for key, value in replacements.items():
        if not isinstance(key, str):
            raise TypeError("all replacement keys must be strings")
        if not isinstance(value, str):
            raise TypeError("all replacement values must be strings")
        if key == "":
            raise ValueError("replacement keys must not be empty strings")
