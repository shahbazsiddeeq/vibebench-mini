import base64

def encode_basic_auth(username: str, password: str) -> str:
    """
    Encodes username and password into an HTTP Basic Authorization header value.

    Args:
        username: The username string. Must not contain a colon ':'.
        password: The password string. May contain colons.

    Returns:
        A string representing the HTTP Basic Authorization header value,
        e.g., 'Basic QWxhZGRpbjpvcGVuOnNlc2FtZQ=='.

    Raises:
        ValueError: If the username contains a colon ':'.
    """
    if ':' in username:
        raise ValueError("Username must not contain a colon (':').")

    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('ascii')
    return f"Basic {encoded_credentials}"

def decode_basic_auth(header: str) -> tuple[str, str]:
    """
    Decodes an HTTP Basic Authorization header value into username and password.

    Args:
        header: The HTTP Basic Authorization header value string,
                e.g., 'Basic QWxhZGRpbjpvcGVuOnNlc2FtZQ=='.

    Returns:
        A tuple containing (username, password).

    Raises:
        ValueError: If the header is malformed, the scheme is not 'Basic',
                    the base64 token is invalid, the decoded bytes are not
                    valid UTF-8, or the decoded string does not contain a colon.
    """
    parts = header.split(' ', 1)
    if len(parts) != 2:
        raise ValueError("Invalid Authorization header format: missing scheme or token.")

    scheme, token = parts[0], parts[1]

    if scheme.lower() != 'basic':
        raise ValueError(f"Unsupported authentication scheme: '{scheme}'. Expected 'Basic'.")

    if not token:
        raise ValueError("Authorization token is empty.")

    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except base64.binascii.Error as e:
        raise ValueError(f"Invalid base64 encoding in token: {e}")

    try:
        decoded_credentials = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Invalid UTF-8 encoding in decoded credentials.")

    # Split on the first colon only
    split_credentials = decoded_credentials.split(':', 1)

    if len(split_credentials) != 2:
        raise ValueError("Decoded credentials do not contain a colon (':') separator.")

    username, password = split_credentials[0], split_credentials[1]

    return username, password
