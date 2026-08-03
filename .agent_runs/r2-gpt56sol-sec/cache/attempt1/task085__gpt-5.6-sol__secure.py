"""Utilities for building URL query strings."""

from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import urlencode


def build_query(params: Mapping[str, object]) -> str:
    """Build a deterministically ordered URL query string.

    List values are encoded as repeated keys, while spaces are encoded as
    ``+`` according to application/x-www-form-urlencoded rules.
    """
    if not isinstance(params, Mapping):
        raise TypeError("params must be a mapping")

    for key in params:
        if not isinstance(key, str):
            raise TypeError("query parameter keys must be strings")

    ordered_items = sorted(params.items(), key=lambda item: item[0])
    return urlencode(ordered_items, doseq=True)
