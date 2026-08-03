"""
src/solution.py

Provides `assert_dict_subset`, a security-conscious helper for verifying
that one dictionary's key/value pairs form a subset of another dictionary's
key/value pairs.

Design notes:
- No use of eval/exec or any dynamic code execution.
- No I/O, no external data sources, no randomness needed for this task.
- Inputs are strictly validated; informative but non-sensitive error
  messages are produced (no internal state, stack traces, or secrets are
  leaked in exceptions).
- All mismatches are collected before raising, as required by the spec.
"""

from typing import Any, Dict, Hashable


def _safe_repr(value: Any) -> str:
    """
    Produce a safe, bounded string representation of a value for inclusion
    in error messages. Avoids extremely long output which could be used
    to flood logs or obscure other information.
    """
    try:
        text = repr(value)
    except Exception:
        # Fall back to a generic placeholder if repr() itself fails.
        text = f"<unrepresentable {type(value).__name__}>"

    max_len = 200
    if len(text) > max_len:
        text = text[:max_len] + "...(truncated)"
    return text


def assert_dict_subset(actual: Dict[Hashable, Any], expected: Dict[Hashable, Any]) -> None:
    """
    Assert that every key/value pair in `expected` is present in `actual`
    with an equal value. Extra keys in `actual` are ignored.

    Parameters
    ----------
    actual : dict
        The dictionary being checked.
    expected : dict
        The dictionary whose entries must all be present (as a subset)
        in `actual`.

    Returns
    -------
    None
        If `expected` is a subset of `actual` (key-wise and value-wise).

    Raises
    ------
    AssertionError
        If one or more key/value pairs in `expected` are missing from or
        differ from those in `actual`. The exception message contains one
        line per mismatch:
          - "Missing key: <key>" for keys absent from `actual`.
          - A line containing "expected" along with the expected and
            actual values for keys whose values differ.
    TypeError
        If `actual` or `expected` is not a dict instance.
    """
    if not isinstance(actual, dict):
        raise TypeError("actual must be a dict")
    if not isinstance(expected, dict):
        raise TypeError("expected must be a dict")

    mismatches = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key: {_safe_repr(key)}")
            continue

        actual_value = actual[key]
        try:
            values_equal = actual_value == expected_value
        except Exception:
            # If comparison itself raises, treat as a mismatch rather than
            # propagating an unrelated exception type.
            values_equal = False

        if not values_equal:
            mismatches.append(
                f"Key {_safe_repr(key)}: expected {_safe_repr(expected_value)}, "
                f"got {_safe_repr(actual_value)}"
            )

    if mismatches:
        raise AssertionError("\n".join(mismatches))
