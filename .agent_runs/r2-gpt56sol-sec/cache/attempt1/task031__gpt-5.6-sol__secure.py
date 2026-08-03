"""Utilities for flattening nested lists."""

from typing import Any


def flatten(nested: Any) -> list[Any]:
    """Return a list containing all non-list values from nested lists.

    Only instances of ``list`` are flattened. Other iterable values, such as
    tuples and strings, are preserved unchanged. Cyclic list structures are
    rejected.
    """
    if not isinstance(nested, list):
        return [nested]

    result: list[Any] = []
    active_ids = {id(nested)}
    stack: list[tuple[object, int]] = [(iter(nested), id(nested))]

    while stack:
        iterator, list_id = stack[-1]

        try:
            item = next(iterator)  # type: ignore[arg-type]
        except StopIteration:
            stack.pop()
            active_ids.remove(list_id)
            continue

        if isinstance(item, list):
            item_id = id(item)
            if item_id in active_ids:
                raise ValueError("cyclic nested list cannot be flattened")
            active_ids.add(item_id)
            stack.append((iter(item), item_id))
        else:
            result.append(item)

    return result
