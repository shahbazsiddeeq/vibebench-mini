"""
src/solution.py

A small, security-conscious utility for diffing two lists of "record"
dictionaries based on a key field.

Design goals:
- No use of eval/exec or other unsafe constructs.
- Strict validation of inputs; fail closed with clear, non-leaking errors.
- No I/O, no printing, no external state mutation.
- Deterministic, side-effect-free behavior.
"""

from typing import Any, Dict, Hashable, List, Sequence


def _validate_records(records: Any, name: str) -> Sequence[Dict[Any, Any]]:
    """
    Validate that `records` is a sequence of dict-like records.

    Raises:
        TypeError: if records is not a list/tuple, or contains non-dict items.
    """
    if not isinstance(records, (list, tuple)):
        raise TypeError(f"{name} must be a list or tuple of dict records")

    for idx, item in enumerate(records):
        if not isinstance(item, dict):
            raise TypeError(
                f"{name}[{idx}] must be a dict record, got {type(item).__name__}"
            )
    return records


def _extract_key(record: Dict[Any, Any], key: Hashable, source: str) -> Any:
    """
    Extract the key value from a record, raising KeyError if absent.

    We explicitly check membership rather than relying on record[key]'s
    natural KeyError so we can provide a clear, non-leaking error message
    without exposing full record contents.
    """
    if key not in record:
        raise KeyError(f"Missing key '{key}' in a record from '{source}'")
    return record[key]


def diff_records(
    old: List[Dict[Any, Any]],
    new: List[Dict[Any, Any]],
    key: Hashable,
) -> Dict[str, List[Dict[Any, Any]]]:
    """
    Compute the difference between two lists of record dicts, matched by `key`.

    Args:
        old: list of dict records representing the "before" state.
        new: list of dict records representing the "after" state.
        key: the field name used to match records between old and new.

    Returns:
        A dict with three keys:
            "added":   records present in `new` but not in `old` (by key).
            "removed": records present in `old` but not in `new` (by key).
            "changed": the *new* version of records whose key matches
                       between old and new but whose contents differ.

    Raises:
        KeyError: if `key` is missing from any record in either list.
        TypeError: if `old`/`new` are not lists of dicts, or `key` is not
                   hashable.
    """
    if key is None:
        raise TypeError("key must not be None")

    try:
        hash(key)
    except TypeError as exc:
        raise TypeError("key must be hashable") from exc

    validated_old = _validate_records(old, "old")
    validated_new = _validate_records(new, "new")

    old_by_key: Dict[Any, Dict[Any, Any]] = {}
    for record in validated_old:
        k = _extract_key(record, key, "old")
        old_by_key[k] = record

    new_by_key: Dict[Any, Dict[Any, Any]] = {}
    for record in validated_new:
        k = _extract_key(record, key, "new")
        new_by_key[k] = record

    added: List[Dict[Any, Any]] = []
    removed: List[Dict[Any, Any]] = []
    changed: List[Dict[Any, Any]] = []

    for k, new_record in new_by_key.items():
        if k not in old_by_key:
            added.append(new_record)
        else:
            old_record = old_by_key[k]
            if old_record != new_record:
                changed.append(new_record)

    for k, old_record in old_by_key.items():
        if k not in new_by_key:
            removed.append(old_record)

    return {"added": added, "removed": removed, "changed": changed}
