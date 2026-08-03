import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://")


def _remove_dot_segments(path: str) -> str:
    """Resolve '.'/'..' segments and collapse consecutive slashes."""
    leading = path.startswith("/")
    trailing = path.endswith("/") and len(path) > 1
    parts: list[str] = []
    for seg in path.split("/"):
        if seg in ("", "."):
            continue
        if seg == "..":
            if parts:
                parts.pop()
            continue
        parts.append(seg)
    out = "/".join(parts)
    if leading:
        out = "/" + out
    if trailing and not out.endswith("/"):
        out += "/"
    return out


def normalize_url(url: str) -> str:
    url = url.strip()
    # urlsplit drops a bare host into the path when no scheme is present, so
    # prepend the default scheme before splitting.
    if not _SCHEME_RE.match(url):
        url = "https://" + url

    s = urlsplit(url)
    scheme = s.scheme.lower()

    # host + port normalization
    hostname = (s.hostname or "").lower()
    port = s.port
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None

    auth = ""
    if s.username:
        auth = s.username
        if s.password:
            auth += f":{s.password}"
        auth += "@"

    netloc = auth + hostname + (f":{port}" if port else "")

    # path: resolve dot-segments, collapse slashes, empty -> "/"
    path = _remove_dot_segments(s.path) or "/"

    # query: sort params for stability (blank values kept)
    q_items = parse_qsl(s.query, keep_blank_values=True)
    query = urlencode(sorted(q_items), doseq=True)

    return urlunsplit((scheme, netloc, path, query, ""))  # drop fragment
