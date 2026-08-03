"""
src/solution.py

A secure, self-contained URL normalizer.

normalize_url(url) returns a canonical form of a URL according to the
following rules:
    1. If the input has no scheme, default to "https".
    2. Lowercase the scheme and the host. Userinfo ("user:pass@") is
       preserved verbatim (case kept).
    3. Drop the default port for the scheme (80 for http, 443 for https);
       keep any other port.
    4. Normalize the path: resolve "." and ".." dot-segments and collapse
       runs of consecutive slashes into one. An empty path becomes "/".
       A trailing slash is preserved.
    5. Sort the query parameters by key (blank values are kept, e.g. "a=").
    6. Drop the fragment.

Only the Python standard library is used. No eval/exec is used anywhere.
Errors are surfaced as ValueError with generic, non-leaking messages.
"""

from __future__ import annotations

import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

__all__ = ["normalize_url"]

# A conservative pattern for a valid URI scheme (RFC 3986).
_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*$")

# Default ports for schemes we know how to normalize.
_DEFAULT_PORTS = {
    "http": "80",
    "https": "443",
}

_MAX_URL_LENGTH = 8192  # sane upper bound to avoid abuse / resource exhaustion


def _fail(message: str = "Invalid URL") -> None:
    """Raise a ValueError without leaking internal details."""
    raise ValueError(message)


def _normalize_path(path: str) -> str:
    """
    Normalize a URL path: collapse multiple slashes, resolve '.' and '..'
    dot-segments, and preserve/restore a trailing slash. An empty path
    becomes "/".
    """
    if path == "":
        return "/"

    trailing_slash = path.endswith("/")

    segments = path.split("/")
    resolved: list[str] = []

    for seg in segments:
        if seg == "" or seg == ".":
            continue
        elif seg == "..":
            if resolved:
                resolved.pop()
            # if resolved is empty, silently ignore extra ".." (can't go
            # above root) -- this avoids leaking path-traversal artifacts.
        else:
            resolved.append(seg)

    new_path = "/" + "/".join(resolved)

    if trailing_slash and not new_path.endswith("/"):
        new_path += "/"

    if new_path == "":
        new_path = "/"

    return new_path


def _normalize_query(query: str) -> str:
    """
    Parse the query string, keep blank values, sort by key (stable), and
    re-encode.
    """
    if query == "":
        return ""

    pairs = parse_qsl(query, keep_blank_values=True, strict_parsing=False)
    # Stable sort by key only, preserving relative order of equal keys.
    sorted_pairs = sorted(pairs, key=lambda kv: kv[0])
    return urlencode(sorted_pairs)


def _split_netloc(netloc: str) -> tuple[str, str, str]:
    """
    Split a netloc into (userinfo_including_at, host, port).
    Userinfo is preserved verbatim (including trailing '@' if present).
    Host and port are returned separately (port may be an empty string).
    """
    if "@" in netloc:
        userinfo, hostport = netloc.rsplit("@", 1)
        userinfo = userinfo + "@"
    else:
        userinfo = ""
        hostport = netloc

    # Handle IPv6 literal hosts in brackets, e.g. "[::1]:8080".
    if hostport.startswith("["):
        end = hostport.find("]")
        if end == -1:
            _fail()
        host = hostport[: end + 1]
        rest = hostport[end + 1 :]
        if rest.startswith(":"):
            port = rest[1:]
        elif rest == "":
            port = ""
        else:
            _fail()
    else:
        if ":" in hostport:
            host, port = hostport.rsplit(":", 1)
        else:
            host, port = hostport, ""

    if port and not port.isdigit():
        _fail()

    return userinfo, host, port


def normalize_url(url: str) -> str:
    """
    Return a canonical form of `url` according to the module-level rules.

    Raises:
        ValueError: if the input is not a usable URL string.
    """
    if not isinstance(url, str):
        _fail()

    url = url.strip()

    if not url:
        _fail()

    if len(url) > _MAX_URL_LENGTH:
        _fail()

    # Reject embedded control characters / whitespace that could be used
    # for header injection or other trickery.
    if any(ord(ch) < 0x20 for ch in url):
        _fail()

    working_url = url
    if "://" not in working_url:
        working_url = "https://" + working_url

    try:
        parts = urlsplit(working_url)
    except ValueError:
        _fail()

    scheme = parts.scheme.lower() if parts.scheme else "https"
    if not _SCHEME_RE.match(scheme):
        _fail()

    if not parts.netloc:
        _fail()

    userinfo, host, port = _split_netloc(parts.netloc)

    if not host:
        _fail()

    host = host.lower()

    default_port = _DEFAULT_PORTS.get(scheme)
    if port and default_port is not None and port == default_port:
        port = ""

    netloc_norm = f"{userinfo}{host}"
    if port:
        netloc_norm += f":{port}"

    path_norm = _normalize_path(parts.path)
    query_norm = _normalize_query(parts.query)

    # Fragment is always dropped.
    result = urlunsplit((scheme, netloc_norm, path_norm, query_norm, ""))
    return result
