"""
src/solution.py

A secure, self-contained URL parser.

parse_url(url) -> dict with keys:
    scheme, host, port (int or None), path, query_params (dict), fragment

Raises ValueError if the scheme or host is missing, or if the URL is malformed.
"""

from __future__ import annotations

from urllib.parse import urlsplit, parse_qsl
from typing import Any, Dict, List, Union


def parse_url(url: str) -> Dict[str, Any]:
    """
    Parse a URL string into its components.

    :param url: The URL to parse.
    :return: A dict with keys scheme, host, port, path, query_params, fragment.
    :raises ValueError: If input is invalid, or scheme/host is missing.
    """
    if not isinstance(url, str):
        raise ValueError("URL must be a string")

    # Guard against absurdly long input (basic DoS mitigation) without
    # leaking internal details in the error message.
    if len(url) > 8192:
        raise ValueError("URL is too long")

    stripped = url.strip()
    if not stripped:
        raise ValueError("URL must not be empty")

    try:
        parts = urlsplit(stripped)
    except ValueError:
        # urlsplit can raise ValueError for malformed input (e.g. bad port)
        raise ValueError("Malformed URL")

    scheme = parts.scheme
    if not scheme:
        raise ValueError("URL is missing a scheme")

    host = parts.hostname
    if not host:
        raise ValueError("URL is missing a host")

    host = host.lower()

    # Port validation: urlsplit already raises ValueError for non-numeric
    # ports, but we guard again defensively.
    try:
        port = parts.port
    except ValueError:
        raise ValueError("Invalid port in URL")

    if port is not None and not (0 <= port <= 65535):
        raise ValueError("Port out of valid range")

    path = parts.path if parts.path else "/"

    query_params: Dict[str, Union[str, List[str]]] = {}
    if parts.query:
        pairs = parse_qsl(parts.query, keep_blank_values=True)
        collected: Dict[str, List[str]] = {}
        for key, value in pairs:
            if value == "":
                # Drop blank/missing values
                continue
            collected.setdefault(key, []).append(value)

        for key, values in collected.items():
            if len(values) == 1:
                query_params[key] = values[0]
            else:
                query_params[key] = values

    fragment = parts.fragment if parts.fragment else ""

    return {
        "scheme": scheme,
        "host": host,
        "port": port,
        "path": path,
        "query_params": query_params,
        "fragment": fragment,
    }
