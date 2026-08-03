import base64

def encode_basic_auth(username: str, password: str) -> str:
    if ':' in username:
        raise ValueError("Username must not contain ':'")
    
    credentials = f"{username}:{password}"
    credentials_bytes = credentials.encode('utf-8')
    base64_bytes = base64.b64encode(credentials_bytes)
    base64_str = base64_bytes.decode('ascii')
    
    return f"Basic {base64_str}"

def decode_basic_auth(header: str) -> tuple[str, str]:
    if not header.lower().startswith('basic '):
        raise ValueError("Header must start with 'Basic '")
    
    base64_str = header[6:].strip()
    if not base64_str:
        raise ValueError("Missing or empty base64 token")
    
    try:
        base64_bytes = base64.b64decode(base64_str, validate=True)
    except (base64.binascii.Error, ValueError):
        raise ValueError("Invalid base64 encoding")
    
    try:
        credentials = base64_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Decoded bytes are not valid UTF-8")
    
    if ':' not in credentials:
        raise ValueError("Decoded string must contain ':'")
    
    username, password = credentials.split(':', 1)
    return username, password
