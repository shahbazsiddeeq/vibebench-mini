import base64
import json

def decode_jwt_header(token: str) -> dict:
    # Split the token into parts
    parts = token.split('.')
    
    # Ensure there are at least two parts (header and payload)
    if len(parts) < 2:
        raise ValueError("Token must contain at least one '.' character.")
    
    # Get the header part
    header_b64 = parts[0]
    
    # Add padding to the base64 string if necessary
    padding_needed = len(header_b64) % 4
    if padding_needed:
        header_b64 += '=' * (4 - padding_needed)
    
    try:
        # Decode the base64url encoded header
        header_bytes = base64.urlsafe_b64decode(header_b64)
    except (base64.binascii.Error, ValueError):
        raise ValueError("Header is not valid base64url.")
    
    try:
        # Parse the JSON header
        header_json = json.loads(header_bytes)
    except json.JSONDecodeError:
        raise ValueError("Header is not valid JSON.")
    
    # Ensure the JSON is an object
    if not isinstance(header_json, dict):
        raise ValueError("Decoded JSON is not an object.")
    
    return header_json
