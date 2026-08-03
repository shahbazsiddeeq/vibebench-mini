from collections.abc import Mapping
from typing import Any


def assert_dict_subset(actual: Mapping[Any, Any], expected: Mapping[Any, Any]) -> None:
    """Assert that every key/value pair in expected is present in actual."""
    mismatches: list[str] = []

    for key, expected_value in expected.items():
        if key not in actual:
            mismatches.append(f"Missing key {key!r}")
            continue

        actual_value = actual[key]
        if actual_value != expected_value:
            mismatches.append(
                f"Key {key!r}: expected {expected_value!r}, actual {actual_value!r}"
            )

    if mismatches:
        raise AssertionError("\n".join(mismatches))
