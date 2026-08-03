from __future__ import annotations

from urllib.parse import parse_qs, urlparse


def parse_url(url: str) -> dict:
    parsed = urlparse(url)
    if not parsed.scheme:
        raise ValueError("URL must have a scheme")
    if not parsed.hostname:
        raise ValueError("URL must have a host")
    port = parsed.port
    query_params = {
        k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()
    }
    return {
        "scheme": parsed.scheme,
        "host": parsed.hostname,
        "port": port,
        "path": parsed.path or "/",
        "query_params": query_params,
        "fragment": parsed.fragment,
    }
