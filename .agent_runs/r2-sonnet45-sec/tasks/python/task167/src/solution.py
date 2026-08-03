import base64


def encode_basic_auth(username: str, password: str) -> str:
    """
    Encode username and password into HTTP Basic Auth header value.
    
    Args:
        username: Username (must not contain ':')
        password: Password (may contain ':')
    
    Returns:
        Authorization header value in format 'Basic <base64>'
    
    Raises:
        ValueError: If username contains ':'
    """
    if not isinstance(username, str):
        raise ValueError("Username must be a string")
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    
    if ':' in username:
        raise ValueError("Username must not contain ':'")
    
    # Form 'username:password'
    credentials = f"{username}:{password}"
    
    # UTF-8 encode
    credentials_bytes = credentials.encode('utf-8')
    
    # Standard base64 encode with padding
    encoded = base64.b64encode(credentials_bytes).decode('ascii')
    
    # Return 'Basic ' + base64
    return f"Basic {encoded}"


def decode_basic_auth(header: str) -> tuple[str, str]:
    """
    Decode HTTP Basic Auth header value.
    
    Args:
        header: Authorization header value (e.g., 'Basic <base64>')
    
    Returns:
        Tuple of (username, password)
    
    Raises:
        ValueError: If header format is invalid, scheme is not 'basic',
                   token is missing/empty, base64 is invalid, bytes are not
                   valid UTF-8, or decoded string contains no ':'
    """
    if not isinstance(header, str):
        raise ValueError("Header must be a string")
    
    # Split on first space to get scheme and token
    parts = header.split(' ', 1)
    
    if len(parts) != 2:
        raise ValueError("Invalid header format")
    
    scheme, token = parts
    
    # Check scheme case-insensitively
    if scheme.lower() != 'basic':
        raise ValueError("Scheme must be 'basic'")
    
    # Check token is not empty
    if not token:
        raise ValueError("Token must not be empty")
    
    # Decode base64 (strict - will raise if invalid)
    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except Exception:
        raise ValueError("Invalid base64 encoding")
    
    # UTF-8 decode
    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Invalid UTF-8 encoding")
    
    # Split on first ':' only
    if ':' not in decoded_str:
        raise ValueError("Decoded credentials must contain ':'")
    
    username, password = decoded_str.split(':', 1)
    
    return (username, password)
