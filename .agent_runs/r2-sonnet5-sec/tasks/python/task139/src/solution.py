"""
src/solution.py

A small, security-conscious utility module implementing `expand_cases`.

The function creates a list of merged dictionaries (base merged with each
override) without mutating the original `base` dictionary and without
performing any unsafe operations (no eval/exec, no external I/O).
"""

from typing import Any, Dict, List, Mapping, Sequence


def expand_cases(base: Mapping[Any, Any], overrides: Sequence[Mapping[Any, Any]]) -> List[Dict[Any, Any]]:
    """
    Expand a base dictionary with a sequence of overrides.

    For each override in `overrides`, produce a new dictionary that is a
    shallow copy of `base` updated with the override's key/value pairs.
    The override's values take precedence on key collisions. The merge is
    shallow: nested mutable objects (e.g., dicts) are not recursively
    merged, they are replaced wholesale if the key appears in the override.

    Parameters
    ----------
    base : Mapping[Any, Any]
        The base dictionary-like object to use as the starting point for
        each result. Must support `dict(base)` (i.e., be a mapping).
    overrides : Sequence[Mapping[Any, Any]]
        A sequence of dictionary-like objects. Each one produces exactly
        one result in the returned list.

    Returns
    -------
    List[Dict[Any, Any]]
        A list of new dictionaries, one per override, each being a fresh
        top-level dict (never an alias of `base` or of any override).

    Raises
    ------
    TypeError
        If `base` is not a mapping, if `overrides` is not a sequence of
        mappings, or if any individual override is not a mapping.
    """
    # Validate `base`
    if not isinstance(base, Mapping):
        raise TypeError("base must be a mapping (e.g., a dict)")

    # Validate `overrides` container type
    if not isinstance(overrides, Sequence) or isinstance(overrides, (str, bytes, bytearray)):
        raise TypeError("overrides must be a sequence (e.g., a list) of mappings")

    results: List[Dict[Any, Any]] = []

    for idx, override in enumerate(overrides):
        if not isinstance(override, Mapping):
            raise TypeError(f"overrides[{idx}] must be a mapping (e.g., a dict)")

        # Start from a fresh shallow copy of base, then apply the override.
        merged: Dict[Any, Any] = dict(base)
        merged.update(override)
        results.append(merged)

    return results
