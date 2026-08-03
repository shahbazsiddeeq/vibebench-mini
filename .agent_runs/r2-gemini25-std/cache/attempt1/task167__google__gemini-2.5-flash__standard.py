import base64

def encode_basic_auth(username: str, password: str) -> str:
    """
    Builds the Authorization header value for HTTP Basic authentication.

    Args:
        username: The username. Must not contain ':'.
        password: The password. May contain ':'.

    Returns:
        The Authorization header value, e.g., 'Basic QWxhZGRpbjpvcGVuOnNlc2FtZQ=='.

    Raises:
        ValueError: If the username contains ':'.
    """
    if ':' in username:
        raise ValueError("Username must not contain ':'")

    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('ascii')
    return f"Basic {encoded_credentials}"

def decode_basic_auth(header: str) -> tuple[str, str]:
    """
    Parses an HTTP Basic authentication header value and returns (username, password).

    Args:
        header: The Authorization header value, e.g., 'Basic QWxhZGRpbjpvcGVuOnNlc2FtZQ=='.

    Returns:
        A tuple containing the username and password.

    Raises:
        ValueError: If the header is malformed, the scheme is not 'Basic',
                    the base64 token is invalid, the decoded bytes are not valid UTF-8,
                    or the decoded string does not contain a ':'.
    """
    parts = header.split(' ', 1)
    if len(parts) != 2:
        raise ValueError("Invalid Basic Auth header format: missing scheme or token")

    scheme, token = parts
    if scheme.lower() != 'basic':
        raise ValueError(f"Unsupported authentication scheme: '{scheme}'. Expected 'Basic'.")
    if not token:
        raise ValueError("Basic Auth token is missing or empty")

    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except (base64.binascii.Error, ValueError) as e:
        raise ValueError(f"Invalid base64 encoding in token: {e}")

    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 encoding in decoded credentials: {e}")

    # Split on the first colon only
    credentials_parts = decoded_str.split(':', 1)
    if len(credentials_parts) != 2:
        raise ValueError("Decoded credentials do not contain a ':' separator")

    username, password = credentials_parts
    return username, password
