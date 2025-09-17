import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def normalize_url(url: str) -> str:
    s = urlsplit(url)
    scheme = (s.scheme or "https").lower()

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

    # path: collapse // -> /
    path = re.sub(r"/{2,}", "/", s.path or "/")

    # query: sort params for stability
    q_items = parse_qsl(s.query, keep_blank_values=True)
    query = urlencode(sorted(q_items), doseq=True)

    return urlunsplit((scheme, netloc, path, query, ""))  # drop fragment
