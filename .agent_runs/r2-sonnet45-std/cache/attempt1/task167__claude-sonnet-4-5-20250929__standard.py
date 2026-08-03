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
    if ':' in username:
        raise ValueError("Username must not contain ':'")
    
    # Form credentials string
    credentials = f"{username}:{password}"
    
    # UTF-8 encode
    credentials_bytes = credentials.encode('utf-8')
    
    # Base64 encode with padding
    b64_bytes = base64.b64encode(credentials_bytes)
    
    # Convert to string
    b64_string = b64_bytes.decode('ascii')
    
    # Return with 'Basic ' prefix
    return f"Basic {b64_string}"


def decode_basic_auth(header: str) -> tuple[str, str]:
    """
    Decode HTTP Basic Auth header value.
    
    Args:
        header: Authorization header value
    
    Returns:
        Tuple of (username, password)
    
    Raises:
        ValueError: If header is invalid
    """
    # Split on first space
    parts = header.split(' ', 1)
    
    if len(parts) != 2:
        raise ValueError("Invalid header format")
    
    scheme, token = parts
    
    # Check scheme (case-insensitive)
    if scheme.lower() != 'basic':
        raise ValueError("Scheme must be 'Basic'")
    
    # Check token is not empty
    if not token:
        raise ValueError("Token is missing or empty")
    
    # Decode base64 (strict)
    try:
        credentials_bytes = base64.b64decode(token, validate=True)
    except Exception:
        raise ValueError("Invalid base64")
    
    # Decode UTF-8
    try:
        credentials = credentials_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Invalid UTF-8")
    
    # Split on first ':' only
    if ':' not in credentials:
        raise ValueError("Credentials must contain ':'")
    
    username, password = credentials.split(':', 1)
    
    return (username, password)
