"""Group records and calculate count, sum, and mean."""

from typing import Any


def group_by_aggregate(
    records: list[dict[str, Any]],
    key_field: str,
    value_field: str,
) -> dict[Any, dict[str, int | float]]:
    """Aggregate numeric record values by a specified key."""
    aggregates: dict[Any, dict[str, int | float]] = {}

    for record in records:
        key = record[key_field]
        value = record[value_field]

        if key not in aggregates:
            aggregates[key] = {"count": 0, "sum": 0.0, "mean": 0.0}

        group = aggregates[key]
        group["count"] += 1
        group["sum"] += value

    for group in aggregates.values():
        group["sum"] = float(group["sum"])
        group["mean"] = float(round(group["sum"] / group["count"], 4))

    return aggregates
