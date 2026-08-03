import base64
import json


def decode_jwt_header(token):
    """
    Decode and return the header of a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        dict: The decoded header as a dictionary
        
    Raises:
        ValueError: If token has no '.', segment is not valid base64url,
                   content is not valid JSON, or decoded JSON is not an object
    """
    # Check if token contains a dot
    if '.' not in token:
        raise ValueError("Token must contain at least one '.'")
    
    # Extract the first segment (header)
    header_segment = token.split('.')[0]
    
    # Add padding if needed
    # Base64 requires length to be multiple of 4
    padding_needed = (4 - len(header_segment) % 4) % 4
    padded_segment = header_segment + '=' * padding_needed
    
    # Decode from base64url
    try:
        decoded_bytes = base64.urlsafe_b64decode(padded_segment)
    except Exception:
        raise ValueError("Invalid base64url encoding")
    
    # Parse JSON
    try:
        decoded_json = json.loads(decoded_bytes)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON content")
    
    # Check if it's a dict (JSON object)
    if not isinstance(decoded_json, dict):
        raise ValueError("Decoded JSON must be an object")
    
    return decoded_json
