from __future__ import annotations

from urllib.parse import urlencode


def build_query(params: dict) -> str:
    if not params:
        return ""
    pairs = []
    for k in sorted(params.keys()):
        v = params[k]
        if isinstance(v, list):
            for item in v:
                pairs.append((k, str(item)))
        else:
            pairs.append((k, str(v)))
    return urlencode(pairs)
