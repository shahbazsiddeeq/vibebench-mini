from __future__ import annotations

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")


def _normalize_netloc(netloc: str, scheme: str) -> str:
    if "@" in netloc:
        userinfo, _, hostport = netloc.rpartition("@")
        prefix = userinfo + "@"
    else:
        prefix = ""
        hostport = netloc

    port_text: str | None = None

    if hostport.startswith("["):
        closing = hostport.find("]")
        if closing >= 0:
            host = hostport[: closing + 1].lower()
            remainder = hostport[closing + 1 :]
            if remainder.startswith(":"):
                port_text = remainder[1:]
            elif remainder:
                host += remainder.lower()
        else:
            host = hostport.lower()
    elif ":" in hostport:
        host, separator, port_text = hostport.rpartition(":")
        if not separator:
            port_text = None
        host = host.lower()
    else:
        host = hostport.lower()

    if port_text is not None:
        default_port = {"http": 80, "https": 443}.get(scheme)
        try:
            port_number = int(port_text)
        except ValueError:
            port_number = None

        if default_port is None or port_number != default_port:
            host += ":" + port_text

    return prefix + host


def _normalize_path(path: str) -> str:
    if not path:
        return "/"

    trailing_slash = path.endswith("/") or path.endswith("/.") or path.endswith("/..")
    segments: list[str] = []

    for segment in path.split("/"):
        if not segment or segment == ".":
            continue
        if segment == "..":
            if segments:
                segments.pop()
            continue
        segments.append(segment)

    normalized = "/" + "/".join(segments)
    if trailing_slash and normalized != "/":
        normalized += "/"
    return normalized


def _normalize_query(query: str) -> str:
    if not query:
        return ""

    parameters = parse_qsl(query, keep_blank_values=True)
    parameters.sort(key=lambda item: item[0])
    return urlencode(parameters, doseq=True)


def normalize_url(url: str) -> str:
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    if url.startswith("//"):
        url = "https:" + url
    elif not _SCHEME_RE.match(url):
        url = "https://" + url

    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    netloc = _normalize_netloc(parts.netloc, scheme)
    path = _normalize_path(parts.path)
    query = _normalize_query(parts.query)

    return urlunsplit((scheme, netloc, path, query, ""))
