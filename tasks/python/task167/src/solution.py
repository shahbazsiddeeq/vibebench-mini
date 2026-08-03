import base64
import binascii


def encode_basic_auth(username: str, password: str) -> str:
    """Build an RFC 7617 'Basic' Authorization header value.

    Raises ValueError if the username contains ':' (which would break the
    single-colon separator). The password may contain ':'.
    """
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("username and password must be strings")
    if ":" in username:
        raise ValueError("username must not contain ':'")
    token = base64.b64encode(f"{username}:{password}".encode("utf-8"))
    return "Basic " + token.decode("ascii")


def decode_basic_auth(header: str) -> tuple[str, str]:
    """Parse an RFC 7617 'Basic' Authorization header value.

    The scheme is matched case-insensitively; the credentials are split on
    the first ':' only. Raises ValueError on any malformed input.
    """
    if not isinstance(header, str):
        raise ValueError("header must be a string")
    parts = header.split(" ", 1)
    if len(parts) != 2:
        raise ValueError("header must be 'Basic <token>'")
    scheme, token = parts
    if scheme.lower() != "basic":
        raise ValueError(f"unsupported scheme: {scheme!r}")
    if token == "" or " " in token:
        raise ValueError("invalid base64 token")
    try:
        raw = base64.b64decode(token, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError("invalid base64 token")
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("credentials are not valid UTF-8")
    if ":" not in decoded:
        raise ValueError("credentials must contain ':'")
    username, password = decoded.split(":", 1)
    return username, password
