"""Group-by aggregation utilities."""

from typing import Any


def group_by_aggregate(
    records: list[dict[Any, Any]],
    key_field: Any,
    value_field: Any,
) -> dict[Any, dict[str, int | float]]:
    """Group records and calculate count, sum, and rounded mean."""
    groups: dict[Any, list[Any]] = {}

    for record in records:
        group_key = record[key_field]
        value = record[value_field]

        if group_key in groups:
            groups[group_key][0] += 1
            groups[group_key][1] += value
        else:
            groups[group_key] = [1, value]

    result: dict[Any, dict[str, int | float]] = {}
    for group_key, (count, total) in groups.items():
        total_as_float = float(total)
        result[group_key] = {
            "count": count,
            "sum": total_as_float,
            "mean": round(total_as_float / count, 4),
        }

    return result
