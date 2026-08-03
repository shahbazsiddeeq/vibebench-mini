"""
src/solution.py

A secure, self-contained module providing `build_query`, which builds a
URL query string from a dictionary of parameters.

Design goals:
- No use of eval/exec or other unsafe constructs.
- Strict input validation with clear, non-leaking error messages.
- Deterministic output: keys sorted alphabetically.
- Proper URL encoding using the standard library's urllib.parse,
  with spaces encoded as '+' (application/x-www-form-urlencoded style).
- List values produce repeated keys, each value encoded individually.
"""

from __future__ import annotations

from typing import Any, Iterable, List, Tuple
from urllib.parse import quote_plus


# Types that are acceptable as scalar values for query parameters.
_ALLOWED_SCALAR_TYPES = (str, int, float, bool)


def _validate_key(key: Any) -> str:
    """Ensure the key is a non-empty string; return it unchanged."""
    if not isinstance(key, str):
        raise TypeError("Query parameter keys must be strings.")
    if key == "":
        raise ValueError("Query parameter keys must not be empty.")
    return key


def _scalar_to_str(value: Any) -> str:
    """
    Convert a scalar value (str, int, float, bool) to its string
    representation for encoding. Rejects unsupported types explicitly.
    """
    if isinstance(value, bool):
        # Represent booleans as lowercase true/false for predictability.
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    raise TypeError(
        "Unsupported value type for query parameter; "
        "expected str, int, float, bool, or a list of these."
    )


def _normalize_values(value: Any) -> List[str]:
    """
    Normalize a parameter value into a list of string representations.
    Accepts scalars (str/int/float/bool) or lists/tuples of such scalars.
    """
    if isinstance(value, (list, tuple)):
        result: List[str] = []
        for item in value:
            if isinstance(item, (list, tuple, dict)):
                raise TypeError(
                    "Nested lists or dicts are not supported as query values."
                )
            result.append(_scalar_to_str(item))
        return result
    if isinstance(value, dict):
        raise TypeError("Dict values are not supported as query values.")
    return [_scalar_to_str(value)]


def build_query(params: Any) -> str:
    """
    Build a URL query string from a dictionary of parameters.

    Rules:
    - Keys are sorted alphabetically.
    - List/tuple values produce repeated keys (one per item), each
      URL-encoded individually.
    - Scalar values (str, int, float, bool) are converted to strings
      and URL-encoded.
    - Spaces are encoded as '+' (application/x-www-form-urlencoded style),
      matching `urllib.parse.quote_plus` behavior.
    - Returns an empty string for an empty dict.

    Raises:
        TypeError: if `params` is not a dict, or contains unsupported
                   key/value types.
        ValueError: if a key is an empty string.
    """
    if not isinstance(params, dict):
        raise TypeError("params must be a dict.")

    if not params:
        return ""

    pairs: List[Tuple[str, str]] = []

    # Sort keys alphabetically for deterministic output.
    for key in sorted(params.keys(), key=lambda k: _validate_key(k)):
        validated_key = _validate_key(key)
        values = _normalize_values(params[key])
        for v in values:
            pairs.append((validated_key, v))

    encoded_parts = [
        f"{quote_plus(k)}={quote_plus(v)}" for k, v in pairs
    ]

    return "&".join(encoded_parts)
