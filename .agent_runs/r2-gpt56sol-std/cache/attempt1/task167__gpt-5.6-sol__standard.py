import base64
import binascii


def encode_basic_auth(username: str, password: str) -> str:
    """Return an RFC 7617 Basic Authorization header value."""
    if ":" in username:
        raise ValueError("username must not contain ':'")

    credentials = f"{username}:{password}".encode("utf-8")
    token = base64.b64encode(credentials).decode("ascii")
    return "Basic " + token


def decode_basic_auth(header: str) -> tuple[str, str]:
    """Decode an RFC 7617 Basic Authorization header value."""
    if len(header) < 6 or header[:5].lower() != "basic" or header[5] != " ":
        raise ValueError("invalid Basic authentication scheme")

    token = header[6:]
    if not token:
        raise ValueError("missing Basic authentication token")

    try:
        token_bytes = token.encode("ascii")
        decoded = base64.b64decode(token_bytes, validate=True)
    except (UnicodeEncodeError, binascii.Error, ValueError) as exc:
        raise ValueError("invalid base64 token") from exc

    # Enforce canonical standard Base64, including correct padding.
    if base64.b64encode(decoded) != token_bytes:
        raise ValueError("invalid base64 padding or encoding")

    try:
        credentials = decoded.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("credentials are not valid UTF-8") from exc

    if ":" not in credentials:
        raise ValueError("decoded credentials contain no ':' separator")

    username, password = credentials.split(":", 1)
    return username, password
