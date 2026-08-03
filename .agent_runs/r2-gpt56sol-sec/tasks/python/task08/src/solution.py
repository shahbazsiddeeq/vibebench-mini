"""URL normalization utilities."""

from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

__all__ = ["normalize_url"]

_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
_DEFAULT_PORTS = {"http": 80, "https": 443}
_MAX_QUERY_FIELDS = 10_000


def _normalize_path(path: str) -> str:
    if not path:
        return "/"

    segments: list[str] = []
    for segment in path.split("/"):
        if not segment or segment == ".":
            continue
        if segment == "..":
            if segments:
                segments.pop()
            continue
        segments.append(segment)

    preserve_trailing_slash = (
        path.endswith("/") or path.endswith("/.") or path.endswith("/..")
    )

    normalized = "/" + "/".join(segments)
    if preserve_trailing_slash and normalized != "/":
        normalized += "/"
    return normalized


def _normalize_netloc(netloc: str, scheme: str, port: int | None) -> str:
    at_index = netloc.rfind("@")
    if at_index >= 0:
        userinfo = netloc[: at_index + 1]
        authority = netloc[at_index + 1 :]
    else:
        userinfo = ""
        authority = netloc

    if not authority:
        raise ValueError("invalid URL")

    port_text: str | None = None

    if authority.startswith("["):
        closing = authority.find("]")
        if closing < 0:
            raise ValueError("invalid URL")

        host = authority[: closing + 1]
        suffix = authority[closing + 1 :]
        if suffix:
            if not suffix.startswith(":") or len(suffix) == 1:
                raise ValueError("invalid URL")
            port_text = suffix[1:]
    else:
        if authority.count(":") > 1:
            raise ValueError("invalid URL")
        if ":" in authority:
            host, port_text = authority.rsplit(":", 1)
            if not port_text:
                raise ValueError("invalid URL")
        else:
            host = authority

    if not host:
        raise ValueError("invalid URL")

    normalized_host = host.lower()

    if port_text is not None:
        if not port_text.isascii() or not port_text.isdigit():
            raise ValueError("invalid URL")
        if port is None:
            raise ValueError("invalid URL")
        if _DEFAULT_PORTS.get(scheme) != port:
            normalized_host += ":" + port_text

    return userinfo + normalized_host


def normalize_url(url: str) -> str:
    """Return the canonical form of a hierarchical URL.

    Raises:
        TypeError: If ``url`` is not a string.
        ValueError: If ``url`` is empty or malformed.
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")
    if not url:
        raise ValueError("invalid URL")
    if any(character.isspace() or ord(character) == 127 for character in url):
        raise ValueError("invalid URL")

    try:
        if url.startswith("//"):
            candidate = "https:" + url
        elif _SCHEME_RE.match(url):
            candidate = url
        else:
            candidate = "https://" + url

        parsed = urlsplit(candidate)
        scheme = parsed.scheme.lower()

        if not scheme or not parsed.netloc:
            raise ValueError("invalid URL")

        # Accessing these properties performs additional authority validation.
        if parsed.hostname is None:
            raise ValueError("invalid URL")
        port = parsed.port

        netloc = _normalize_netloc(parsed.netloc, scheme, port)
        path = _normalize_path(parsed.path)

        parameters = parse_qsl(
            parsed.query,
            keep_blank_values=True,
            strict_parsing=False,
            encoding="utf-8",
            errors="strict",
            max_num_fields=_MAX_QUERY_FIELDS,
        )
        parameters.sort(key=lambda item: item[0])
        query = urlencode(parameters, doseq=False, encoding="utf-8", errors="strict")

        return urlunsplit((scheme, netloc, path, query, ""))
    except (ValueError, UnicodeError, OverflowError) as exc:
        raise ValueError("invalid URL") from None
