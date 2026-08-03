import base64

def encode_basic_auth(username: str, password: str) -> str:
    if ':' in username:
        raise ValueError("Username must not contain ':'")
    
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded_credentials}"

def decode_basic_auth(header: str) -> tuple[str, str]:
    if not header.lower().startswith("basic "):
        raise ValueError("Invalid scheme")
    
    token = header[6:]  # Skip "Basic "
    if not token:
        raise ValueError("Token is missing or empty")
    
    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except (ValueError, TypeError):
        raise ValueError("Invalid base64 token")
    
    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Decoded bytes are not valid UTF-8")
    
    if ':' not in decoded_str:
        raise ValueError("Decoded string must contain ':'")
    
    username, password = decoded_str.split(':', 1)
    return username, password
