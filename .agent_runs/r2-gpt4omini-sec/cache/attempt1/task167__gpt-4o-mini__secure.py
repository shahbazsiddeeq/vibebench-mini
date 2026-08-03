# src/solution.py

import base64
import secrets

def encode_basic_auth(username: str, password: str) -> str:
    if ':' in username:
        raise ValueError("Username must not contain ':'")
    
    # Create the credentials string
    credentials = f"{username}:{password}"
    
    # Encode to bytes, then to base64
    encoded_bytes = base64.b64encode(credentials.encode('utf-8'))
    
    # Return the formatted Authorization header value
    return f"Basic {encoded_bytes.decode('utf-8')}"

def decode_basic_auth(header: str) -> tuple[str, str]:
    # Validate the header format
    if not header.lower().startswith("basic "):
        raise ValueError("Invalid scheme; must be 'Basic'")
    
    # Extract the token
    token = header[6:].strip()
    if not token:
        raise ValueError("Token is missing or empty")
    
    # Decode the base64 token
    try:
        decoded_bytes = base64.b64decode(token, validate=True)
    except (ValueError, TypeError):
        raise ValueError("Invalid base64 token")
    
    # Decode to UTF-8
    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Decoded bytes are not valid UTF-8")
    
    # Split on the first ':'
    if ':' not in decoded_str:
        raise ValueError("Decoded string must contain ':'")
    
    username, password = decoded_str.split(':', 1)
    
    return username, password
