"""Utilities for comparing collections of records."""

from collections.abc import Iterable, Mapping
from typing import Any


def diff_records(
    old: Iterable[Mapping[Any, Any]],
    new: Iterable[Mapping[Any, Any]],
    key: Any,
) -> dict[str, list[Mapping[Any, Any]]]:
    """Return records added, removed, or changed between two collections.

    Records are matched by the value of ``key``. Result ordering follows
    ``new`` for added and changed records, and ``old`` for removed records.

    Raises:
        KeyError: If any record does not contain ``key``.
        TypeError: If inputs are invalid or a key value is unhashable.
    """
    if isinstance(old, (str, bytes)) or not isinstance(old, Iterable):
        raise TypeError("old must be an iterable of mappings")
    if isinstance(new, (str, bytes)) or not isinstance(new, Iterable):
        raise TypeError("new must be an iterable of mappings")

    old_records = list(old)
    new_records = list(new)

    for record in old_records + new_records:
        if not isinstance(record, Mapping):
            raise TypeError("each record must be a mapping")
        if key not in record:
            raise KeyError(key)

    old_by_key: dict[Any, Mapping[Any, Any]] = {}
    new_by_key: dict[Any, Mapping[Any, Any]] = {}

    try:
        for record in old_records:
            old_by_key[record[key]] = record
        for record in new_records:
            new_by_key[record[key]] = record
    except TypeError:
        raise TypeError("record key values must be hashable") from None

    added = [
        record for record_key, record in new_by_key.items()
        if record_key not in old_by_key
    ]
    removed = [
        record for record_key, record in old_by_key.items()
        if record_key not in new_by_key
    ]
    changed = [
        record for record_key, record in new_by_key.items()
        if record_key in old_by_key and record != old_by_key[record_key]
    ]

    return {"added": added, "removed": removed, "changed": changed}
