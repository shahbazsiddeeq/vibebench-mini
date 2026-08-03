"""
Group-By Sum and Mean
======================

A small, self-contained utility for grouping a list of dictionaries by a
key field and aggregating a numeric value field within each group.

The implementation is defensive: it validates its inputs strictly and
raises clear, non-leaky exceptions on malformed data, while allowing the
documented `KeyError` for missing fields to propagate unmodified.
"""

from __future__ import annotations

from numbers import Real
from typing import Any, Dict, Hashable, List


def _validate_field_name(field: Any, arg_name: str) -> None:
    """Ensure a field selector is a valid, hashable identifier-like value."""
    if field is None:
        raise ValueError(f"{arg_name} must not be None")
    if not isinstance(field, Hashable):
        raise TypeError(f"{arg_name} must be hashable")


def group_by_aggregate(
    records: List[Dict[Any, Any]],
    key_field: Any,
    value_field: Any,
) -> Dict[Any, Dict[str, Any]]:
    """
    Group `records` by `record[key_field]` and aggregate numeric values at
    `record[value_field]`.

    Parameters
    ----------
    records:
        A list of dictionaries.
    key_field:
        The dictionary key whose value is used to group records.
    value_field:
        The dictionary key whose (numeric) value is aggregated per group.

    Returns
    -------
    dict
        Mapping of group key -> {'count': int, 'sum': float, 'mean': float}.
        Returns {} if `records` is empty.

    Raises
    ------
    TypeError
        If `records` is not a list, if an element is not a dict, or if a
        value at `value_field` is not numeric.
    ValueError
        If `key_field` or `value_field` is None.
    KeyError
        Propagated unmodified if a record is missing `key_field` or
        `value_field`.
    """
    if not isinstance(records, list):
        raise TypeError("records must be a list of dictionaries")

    _validate_field_name(key_field, "key_field")
    _validate_field_name(value_field, "value_field")

    if not records:
        return {}

    sums: Dict[Any, float] = {}
    counts: Dict[Any, int] = {}
    order: List[Any] = []

    for record in records:
        if not isinstance(record, dict):
            raise TypeError("each record must be a dictionary")

        # Intentionally do NOT use .get() so that missing fields raise
        # KeyError naturally, as required by the spec.
        key = record[key_field]
        value = record[value_field]

        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(
                f"value at field {value_field!r} must be numeric, "
                f"got {type(value).__name__}"
            )

        if key not in sums:
            sums[key] = 0.0
            counts[key] = 0
            order.append(key)

        sums[key] += float(value)
        counts[key] += 1

    result: Dict[Any, Dict[str, Any]] = {}
    for key in order:
        total = sums[key]
        count = counts[key]
        mean = round(total / count, 4)
        result[key] = {
            "count": count,
            "sum": float(total),
            "mean": float(mean),
        }

    return result
