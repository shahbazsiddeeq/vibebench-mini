"""Dictionary subset assertion helper."""

from collections.abc import Mapping
from typing import Any


def _safe_repr(value: Any, max_length: int = 1_000) -> str:
    """Return a bounded, single-line representation of a value."""
    try:
        rendered = repr(value)
    except Exception:
        rendered = f"<unrepresentable {type(value).__name__}>"

    rendered = rendered.replace("\r", "\\r").replace("\n", "\\n")
    if len(rendered) > max_length:
        rendered = rendered[: max_length - 3] + "..."
    return rendered


def assert_dict_subset(actual: Mapping[Any, Any],
                       expected: Mapping[Any, Any]) -> None:
    """Assert that every key/value pair in expected is present in actual."""
    if not isinstance(actual, Mapping):
        raise TypeError("actual must be a mapping")
    if not isinstance(expected, Mapping):
        raise TypeError("expected must be a mapping")

    mismatches: list[str] = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key {_safe_repr(key)}")
            continue

        actual_value = actual[key]
        try:
            values_equal = bool(actual_value == expected_value)
        except Exception:
            values_equal = False

        if not values_equal:
            mismatches.append(
                f"Key {_safe_repr(key)}: expected {_safe_repr(expected_value)}, "
                f"actual {_safe_repr(actual_value)}"
            )

    if mismatches:
        raise AssertionError("\n".join(mismatches))
