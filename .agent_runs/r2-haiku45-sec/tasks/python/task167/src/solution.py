import base64
from typing import Tuple


def encode_basic_auth(username: str, password: str) -> str:
    """
    Encode username and password into an HTTP Basic Authentication header value.
    
    Args:
        username: The username (must not contain ':')
        password: The password (may contain ':')
    
    Returns:
        The Authorization header value: 'Basic ' + base64-encoded credentials
    
    Raises:
        ValueError: If username contains ':'
    """
    if not isinstance(username, str) or not isinstance(password, str):
        raise ValueError("Username and password must be strings")
    
    if ':' in username:
        raise ValueError("Username must not contain ':'")
    
    # Form 'username:password'
    credentials = f"{username}:{password}"
    
    # UTF-8 encode
    credentials_bytes = credentials.encode('utf-8')
    
    # Standard base64 encode
    encoded_bytes = base64.b64encode(credentials_bytes)
    encoded_str = encoded_bytes.decode('ascii')
    
    # Return 'Basic ' + base64
    return f"Basic {encoded_str}"


def decode_basic_auth(header: str) -> Tuple[str, str]:
    """
    Decode an HTTP Basic Authentication header value.
    
    Args:
        header: The Authorization header value (e.g., 'Basic QWxhZGRpbjpvcGVu')
    
    Returns:
        A tuple of (username, password)
    
    Raises:
        ValueError: If the header is malformed, scheme is not 'basic',
                   base64 is invalid, UTF-8 decoding fails, or no ':' separator found
    """
    if not isinstance(header, str):
        raise ValueError("Header must be a string")
    
    # Split on the first space
    parts = header.split(' ', 1)
    
    if len(parts) != 2:
        raise ValueError("Invalid header format: missing space separator")
    
    scheme, token = parts
    
    # Check scheme case-insensitively
    if scheme.lower() != 'basic':
        raise ValueError(f"Invalid scheme: expected 'basic', got '{scheme}'")
    
    # Check token is not empty
    if not token:
        raise ValueError("Token is empty")
    
    # Decode base64
    try:
        credentials_bytes = base64.b64decode(token, validate=True)
    except Exception:
        raise ValueError("Invalid base64 token")
    
    # UTF-8 decode
    try:
        credentials_str = credentials_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Credentials are not valid UTF-8")
    
    # Split on the first ':' only
    if ':' not in credentials_str:
        raise ValueError("Credentials must contain ':' separator")
    
    username, password = credentials_str.split(':', 1)
    
    return (username, password)
